import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
import sqlite3
import random
import os

# تنظیمات
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ساخت بات
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
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
                username TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                zp INTEGER DEFAULT 1000,
                gem INTEGER DEFAULT 0,
                power INTEGER DEFAULT 100,
                defense_level INTEGER DEFAULT 1,
                cyber_level INTEGER DEFAULT 1,
                miner_level INTEGER DEFAULT 1,
                miner_balance INTEGER DEFAULT 0,
                last_miner_claim INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

db = Database()

# منوهای اصلی
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👤 پروفایل"), types.KeyboardButton(text="⚔️ حمله")],
            [types.KeyboardButton(text="🛒 فروشگاه"), types.KeyboardButton(text="⛏ ماینر")],
        ],
        resize_keyboard=True
    )
    return keyboard

# سیستم کاربر
def get_user(user_id):
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        db.conn.commit()
        return get_user(user_id)
    return user

def update_user_zp(user_id, amount):
    cursor = db.conn.cursor()
    cursor.execute('UPDATE users SET zp = zp + ? WHERE user_id = ?', (amount, user_id))
    db.conn.commit()

# هندلرهای اصلی
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "✅ بات فعال و آنلاین!\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )
    logger.info(f"✅ کاربر {message.from_user.id} بات رو استارت کرد")

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"👤 **پروفایل شما**\n\n"
        f"⭐ سطح: {user[2]}\n"
        f"💰 ZP: {user[4]:,}\n"
        f"💎 جم: {user[5]}\n"
        f"💪 قدرت: {user[6]}\n"
        f"🛡️ پدافند: سطح {user[7]}",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: types.Message):
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "برای حمله به یک کاربر، روی پیامش ریپلای کنید و بنویسید:\n"
        "<code>حمله سومار</code>\n\n"
        "🎯 **موشک‌های موجود:**\n"
        "• سومار (۱۰۰ دمیج)\n"
        "• زلزله (۲۰۰ دمیج)\n"
        "• آتشفشان (۵۰۰ دمیج)",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: types.Message):
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 موشک‌ها\n"
        "🛩 جنگنده‌ها\n"
        "🛸 پهپادها\n"
        "🔧 پدافند\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"⛏️ **سیستم ماینر**\n\n"
        f"💰 تولید: ۱۰۰ ZP/ساعت\n"
        f"📊 سطح: {user[9]}\n"
        f"💎 موجودی: {user[10]} ZP\n"
        f"🔼 هزینه ارتقا: ۵۰۰ ZP",
        reply_markup=main_menu()
    )

@dp.message()
async def all_messages(message: types.Message):
    if message.text.startswith("حمله "):
        missile_type = message.text.replace("حمله ", "").strip()
        await message.answer(f"🚀 شلیک {missile_type}...\n✅ حمله موفق!")
        update_user_zp(message.from_user.id, 50)
    else:
        await message.answer("🎯 از منوی زیر انتخاب کنید:", reply_markup=main_menu())

# وب‌سرور برای رندر
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"✅ وب‌هوک تنظیم شد: {WEBHOOK_URL}")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot Active! ⚔️")

def main():
    # ساخت اپلیکیشن وب
    app = web.Application()
    
    # ثبت وب‌هوک
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")
    
    # صفحه سلامت
    app.router.add_get("/", health_check)
    
    # رویداد استارتاپ
    app.on_startup.append(on_startup)
    
    logger.info("🚀 شروع وب‌سرور WarZone...")
    web.run_app(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    main()
