import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
import sqlite3
import json
import random
import time
import os

# تنظیمات
TOKEN = os.getenv("TOKEN")
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missiles (
                user_id INTEGER,
                missile_type TEXT,
                quantity INTEGER DEFAULT 0
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
            [types.KeyboardButton(text="📦 جعبه"), types.KeyboardButton(text="🛡 دفاع")],
            [types.KeyboardButton(text="🕵️ خرابکاری"), types.KeyboardButton(text="🎯 ترکیب‌ها")]
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
        cursor.execute('''
            INSERT INTO users (user_id, username) VALUES (?, ?)
        ''', (user_id, ""))
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
        "یک بازی استراتژیک با سیستم حمله و دفاع پیشرفته\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"👤 **پروفایل شما**\n\n"
        f"⭐ سطح: {user[2]}\n"
        f"📊 XP: {user[3]}/100\n"
        f"💰 ZP: {user[4]:,}\n"
        f"💎 جم: {user[5]}\n"
        f"💪 قدرت: {user[6]}\n"
        f"🛡️ پدافند: سطح {user[7]}\n"
        f"🔒 امنیت: سطح {user[8]}\n"
        f"⛏️ ماینر: سطح {user[9]}",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🎯 حمله تکی"), types.KeyboardButton(text="💥 حمله ترکیبی")],
            [types.KeyboardButton(text="📊 تاریخچه حملات"), types.KeyboardButton(text="🔙 منوی اصلی")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "🎯 **حمله تکی** - استفاده از یک موشک\n"
        "💥 **حمله ترکیبی** - ترکیب جنگنده و موشک\n"
        "💰 **سیستم غارت** - کسب ZP از حمله\n\n"
        "👇 نوع حمله را انتخاب کنید:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "🎯 حمله تکی")
async def single_attack_handler(message: types.Message):
    await message.answer(
        "🎯 **حمله تکی**\n\n"
        "برای حمله به یک کاربر، روی پیامش ریپلای کنید و بنویسید:\n"
        "<code>حمله سومار</code>\n\n"
        "🛡️ **موشک‌های موجود:**\n"
        "• سومار (۱۰۰ دمیج) - ۵۰۰ ZP\n"
        "• زلزله (۲۰۰ دمیج) - ۱,۰۰۰ ZP\n"
        "• آتشفشان (۵۰۰ دمیج) - ۲,۰۰۰ ZP",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🚀 موشک‌ها"), types.KeyboardButton(text="🛩 جنگنده")],
            [types.KeyboardButton(text="🛸 پهپاد"), types.KeyboardButton(text="🔧 پدافند")],
            [types.KeyboardButton(text="🔙 منوی اصلی")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 **موشک‌ها** - از عادی تا آخرالزمانی\n"
        "🛩 **جنگنده‌ها** - افزایش قدرت حمله\n"
        "🛸 **پهپادها** - حمله هوایی\n"
        "🔧 **پدافند** - حفاظت از پایگاه\n\n"
        "👇 دسته مورد نظر را انتخاب کنید:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: types.Message):
    user = get_user(message.from_user.id)
    miner_income = user[9] * 100
    await message.answer(
        f"⛏️ **سیستم ماینر**\n\n"
        f"💰 تولید: {miner_income} ZP/ساعت\n"
        f"📊 سطح: {user[9]}\n"
        f"💎 موجودی: {user[10]} ZP\n"
        f"🔼 هزینه ارتقا: {user[9] * 500} ZP\n\n"
        f"⏰ هر ساعت می‌توانید برداشت کنید",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "📦 جعبه")
async def boxes_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📦 جعبه برنزی"), types.KeyboardButton(text="🥈 جعبه نقره‌ای")],
            [types.KeyboardButton(text="🥇 جعبه طلایی"), types.KeyboardButton(text="🔙 منوی اصلی")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "📦 **جعبه‌های شانس**\n\n"
        "📦 **برنزی** - رایگان (هر ۲۴ ساعت)\n"
        "🥈 **نقره‌ای** - ۲,۰۰۰ ZP\n"
        "🥇 **طلایی** - ۵,۰۰۰ ZP\n"
        "💎 **الماس** - ۲ جم\n"
        "🌟 **افسانه‌ای** - ۵ جم\n\n"
        "👇 جعبه مورد نظر را انتخاب کنید:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "🛡 دفاع")
async def defense_handler(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"🛡 **سیستم دفاع**\n\n"
        f"🔒 **پدافند فعلی**: سطح {user[7]}\n"
        f"🛡 **امنیت سایبری**: سطح {user[8]}\n"
        f"💪 **مقاومت**: {user[7] * 15}%\n"
        f"🔓 **هزینه ارتقا**: {user[7] * 1000} ZP\n\n"
        f"🛡️ پدافند باعث کاهش دمیج حملات می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🕵️ خرابکاری")
async def sabotage_handler(message: types.Message):
    await message.answer(
        "🕵️ **سیستم خرابکاری**\n\n"
        "🕵️ **نفوذی** - کاهش پدافند دشمن\n"
        "💻 **الکترونیکی** - غیرفعال کردن سیستم\n"
        "📡 **اطلاعاتی** - افزایش غارت\n\n"
        "💰 **هزینه‌ها:**\n"
        "• نفوذی: ۵۰۰ ZP\n"
        "• الکترونیکی: ۱,۲۰۰ ZP\n"
        "• اطلاعاتی: ۲,۰۰۰ ZP\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🎯 ترکیب‌ها")
async def combo_handler(message: types.Message):
    await message.answer(
        "🎯 **ترکیب‌های حمله**\n\n"
        "🛠 **ترکیب ۱** - حمله سریع\n"
        "🛠 **ترکیب ۲** - حمله سنگین\n"
        "🛠 **ترکیب ۳** - حمله ویژه\n\n"
        "💡 می‌توانید ۳ ترکیب مختلف بسازید\n"
        "🎯 با دستور سریع حمله کنید\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🔙 منوی اصلی")
async def back_to_main(message: types.Message):
    await message.answer("🔙 بازگشت به منوی اصلی", reply_markup=main_menu())

# هندلر پیام‌های معمولی
@dp.message()
async def all_messages(message: types.Message):
    if message.text.startswith("حمله "):
        missile_type = message.text.replace("حمله ", "").strip()
        await message.answer(f"🚀 در حال شلیک {missile_type}...\n\nحمله موفقیت‌آمیز بود! 🎯")
        update_user_zp(message.from_user.id, 100)  # جایزه حمله
    else:
        await message.answer("🤖 از منوی زیر انتخاب کنید:", reply_markup=main_menu())

# شروع بات
async def main():
    logger.info("🚀 شروع بات WarZone...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
