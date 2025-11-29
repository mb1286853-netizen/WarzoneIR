import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
import sqlite3
import os

# تنظیمات
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ساخت بات با تنظیمات جدید
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# دیتابیس ساده
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('warzone.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                zp INTEGER DEFAULT 1000,
                gem INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

db = Database()

def get_user(user_id):
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        db.conn.commit()
        return get_user(user_id)
    return user

def update_zp(user_id, amount):
    cursor = db.conn.cursor()
    cursor.execute('UPDATE users SET zp = zp + ? WHERE user_id = ?', (amount, user_id))
    db.conn.commit()

# منوی اصلی
def main_menu():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👤 پروفایل"), types.KeyboardButton(text="⚔️ حمله")],
            [types.KeyboardButton(text="🛒 فروشگاه"), types.KeyboardButton(text="⛏ ماینر")],
        ],
        resize_keyboard=True
    )

# هندلرها
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "✅ بات فعال و آنلاین!\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )
    logger.info(f"✅ کاربر {message.from_user.id} استارت زد")

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"👤 **پروفایل شما**\n\n"
        f"⭐ سطح: {user[1]}\n"
        f"💰 ZP: {user[3]:,}\n"
        f"💎 جم: {user[4]}",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: types.Message):
    update_zp(message.from_user.id, 50)
    await message.answer(
        "⚔️ **حمله موفق!** 🎯\n\n"
        "💰 +۵۰ ZP دریافت کردید!\n\n"
        "برای حمله واقعی، روی پیام کاربر ریپلای کن و بنویس:\n"
        "<code>حمله</code>",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: types.Message):
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 موشک‌ها\n"
        "🛩 جنگنده‌ها\n"
        "🛸 پهپادها\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: types.Message):
    await message.answer(
        "⛏ **سیستم ماینر**\n\n"
        "💰 تولید خودکار ZP\n"
        "📊 قابل ارتقا تا سطح ۱۵\n"
        "⏰ برداشت هر ۳ ساعت\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message()
async def all_messages(message: types.Message):
    if "حمله" in message.text.lower():
        update_zp(message.from_user.id, 30)
        await message.answer("🚀 حمله انجام شد! 💰 +۳۰ ZP", reply_markup=main_menu())
    else:
        await message.answer("🎯 از منوی زیر انتخاب کنید:", reply_markup=main_menu())

# وب‌سرور
async def on_startup(app):
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/webhook"
    await bot.set_webhook(webhook_url)
    logger.info("✅ وب‌هوک تنظیم شد")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot Active! ⚔️")

def main():
    app = web.Application()
    
    # وب‌هوک
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")
    
    # سلامت
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    
    # استارتاپ
    app.on_startup.append(on_startup)
    
    logger.info(f"🚀 شروع سرور روی پورت {PORT}...")
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == '__main__':
    main()
