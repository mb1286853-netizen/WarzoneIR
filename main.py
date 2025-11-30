import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import sqlite3
import os

# تنظیمات
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🚀 شروع راه‌اندازی بات WarZone...")
print(f"🔑 توکن: {'وجود دارد' if TOKEN else 'وجود ندارد'}")
print("=" * 50)

if not TOKEN:
    print("❌ توکن پیدا نشد!")
    exit()

# ساخت بات
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
    print(f"✅ کاربر {message.from_user.id} استارت زد")

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
    print(f"📊 پروفایل کاربر {message.from_user.id}")

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: types.Message):
    update_zp(message.from_user.id, 50)
    await message.answer(
        "⚔️ **حمله موفق!** 🎯\n\n"
        "💰 +۵۰ ZP دریافت کردید!\n\n"
        "برای حمله به کاربران دیگر، روی پیامشون ریپلای کن و بنویس:\n"
        "<code>حمله</code>",
        reply_markup=main_menu()
    )
    print(f"⚔️ حمله کاربر {message.from_user.id}")

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
        print(f"🎯 حمله کاربر {message.from_user.id}")
    else:
        await message.answer("🎯 از منوی زیر انتخاب کنید:", reply_markup=main_menu())

# شروع بات
async def main():
    print("🔄 اتصال به تلگرام...")
    
    # حذف وب‌هوک قبلی
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ وب‌هوک‌های قبلی حذف شد")
    except:
        print("⚠️ مشکل در حذف وب‌هوک")
    
    # اطلاعات بات
    bot_info = await bot.get_me()
    print(f"✅ بات: @{bot_info.username}")
    print("🚀 بات فعال شد! منتظر پیام...")
    
    # شروع polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ خطا: {e}")
