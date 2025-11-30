import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiohttp
import os
import time

# تنظیمات
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🚀 شروع راه‌اندازی بات WarZone...")
print("=" * 50)

if not TOKEN:
    print("❌ توکن پیدا نشد!")
    exit()

# ساخت بات
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

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
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "✅ بات فعال و آنلاین!\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )
    print(f"✅ کاربر {message.from_user.id} استارت زد")

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: types.Message):
    await message.answer(
        "👤 **پروفایل شما**\n\n"
        "⭐ سطح: ۱\n"
        "💰 ZP: ۱,۰۰۰\n"
        "💎 جم: ۰\n"
        "💪 قدرت: ۱۰۰",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: types.Message):
    await message.answer(
        "⚔️ **حمله موفق!** 🎯\n\n"
        "💰 +۵۰ ZP دریافت کردید!\n\n"
        "برای حمله واقعی روی پیام کاربر ریپلای کن: حمله",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: types.Message):
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 موشک‌ها\n🛩 جنگنده‌ها\n🛸 پهپادها\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: types.Message):
    await message.answer(
        "⛏ **سیستم ماینر**\n\n"
        "💰 تولید خودکار ZP\n📊 قابل ارتقا\n⏰ برداشت دوره‌ای\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message()
async def all_messages(message: types.Message):
    if "حمله" in message.text.lower():
        await message.answer("🚀 حمله انجام شد! 💰 +۳۰ ZP", reply_markup=main_menu())
    else:
        await message.answer("🎯 از منوی زیر انتخاب کنید:", reply_markup=main_menu())

async def ensure_single_instance():
    """مطمئن شو فقط یک نمونه بات در حال اجراست"""
    async with aiohttp.ClientSession() as session:
        # حذف کامل وب‌هوک
        url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
        async with session.get(url) as response:
            result = await response.json()
            print(f"🗑️ حذف وب‌هوک: {result}")
        
        # صبر کن مطمئن شو حذف شده
        await asyncio.sleep(2)
        
        # تأیید حذف
        url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
        async with session.get(url) as response:
            webhook_info = await response.json()
            print(f"🔍 وضعیت وب‌هوک: {webhook_info}")

async def main():
    print("🔄 راه‌اندازی بات...")
    
    try:
        # مطمئن شو فقط یک نمونه اجراست
        await ensure_single_instance()
        
        # اطلاعات بات
        bot_info = await bot.get_me()
        print(f"✅ بات: @{bot_info.username}")
        
        print("🚀 شروع دریافت پیام‌ها...")
        
        # شروع polling با مدیریت بهتر
        await dp.start_polling(bot, skip_updates=True, allowed_updates=["message"])
        
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == '__main__':
    # فقط یک نمونه اجرا شود
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⏹️ بات متوقف شد")
    except Exception as e:
        print(f"💥 خطای بحرانی: {e}")
