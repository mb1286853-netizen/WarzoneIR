import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not TOKEN:
    logger.error("❌ توکن پیدا نشد!")
    exit()

logger.info("🔄 ایجاد Bot instance...")

# ساخت Bot
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 پروفایل"), KeyboardButton(text="⚔️ حمله")],
            [KeyboardButton(text="🛒 فروشگاه"), KeyboardButton(text="⛏ ماینر")],
            [KeyboardButton(text="📦 جعبه"), KeyboardButton(text="🛡 دفاع")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user = message.from_user
    logger.info(f"🎯 START از: {user.id} (@{user.username})")
    
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "✅ بات فعال و آنلاین!\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )
    logger.info("✅ پاسخ ارسال شد!")

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: Message):
    logger.info(f"📊 پروفایل از: {message.from_user.id}")
    await message.answer(
        "👤 **پروفایل شما**\n\n"
        "⭐ سطح: ۱\n💰 ZP: ۱,۰۰۰\n💎 جم: ۰\n"
        "💪 قدرت: ۱۰۰\n🛡️ پدافند: سطح ۱\n\n"
        "📈 با حمله کردن پیشرفت کنید!",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: Message):
    logger.info(f"⚔️ حمله از: {message.from_user.id}")
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "🎯 حمله تکی\n💥 حمله ترکیبی\n💰 سیستم غارت\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: Message):
    logger.info(f"🛒 فروشگاه از: {message.from_user.id}")
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 موشک‌ها\n🛩 جنگنده‌ها\n🛸 پهپادها\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: Message):
    logger.info(f"⛏ ماینر از: {message.from_user.id}")
    await message.answer(
        "⛏ **سیستم ماینر**\n\n"
        "💰 تولید: ۱۰۰ ZP/۳ساعت\n📊 سطح: ۱\n\n"
        "⏰ هر ۳ ساعت برداشت کنید",
        reply_markup=main_menu()
    )

@dp.message()
async def all_messages(message: Message):
    logger.info(f"📩 پیام: '{message.text}'")
    await message.answer(
        "🤖 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )

async def main():
    logger.info("🚀 شروع بات WarZone...")
    
    # اطلاعات بات
    bot_info = await bot.get_me()
    logger.info(f"✅ بات: @{bot_info.username}")
    
    # شروع polling
    logger.info("🔄 شروع دریافت پیام‌ها...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ بات متوقف شد")
    except Exception as e:
        logger.error(f"❌ خطا: {e}")
