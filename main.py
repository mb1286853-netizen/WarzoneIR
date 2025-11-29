import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

# رفع باگ asyncio برای رندر
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not TOKEN:
    logger.error("❌ توکن پیدا نشد!")
    exit()

logger.info("🔄 ایجاد Bot instance...")

# ساخت Bot با تنظیمات ساده‌تر
bot = Bot(token=TOKEN)
dp = Dispatcher()

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 پروفایل"), KeyboardButton(text="⚔️ حمله")],
            [KeyboardButton(text="🛒 فروشگاه"), KeyboardButton(text="⛏ ماینر")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user = message.from_user
    logger.info(f"🎯 دریافت /start از کاربر: {user.id}")
    
    # ارسال پیام ساده بدون مشکل timeout
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "✅ بات فعال است!\n"
        "👇 از منو استفاده کنید:",
        reply_markup=main_menu()
    )
    logger.info("✅ پاسخ ارسال شد!")

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: Message):
    logger.info(f"📊 پروفایل از: {message.from_user.id}")
    await message.answer(
        "👤 **پروفایل شما**\n\n⭐ سطح: ۱\n💰 ZP: ۱,۰۰۰\n💎 جم: ۰\n💪 قدرت: ۱۰۰",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: Message):
    logger.info(f"⚔️ حمله از: {message.from_user.id}")
    await message.answer(
        "⚔️ **سیستم حمله**\n\n🎯 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: Message):
    logger.info(f"🛒 فروشگاه از: {message.from_user.id}")
    await message.answer(
        "🛒 **فروشگاه**\n\nبه زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: Message):
    logger.info(f"⛏ ماینر از: {message.from_user.id}")
    await message.answer(
        "⛏ **ماینر**\n\nبه زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message()
async def echo_handler(message: Message):
    logger.info(f"📩 پیام: '{message.text}'")
    await message.answer("🤖 از منو استفاده کنید:", reply_markup=main_menu())

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active! ⚔️")

async def on_startup():
    bot_info = await bot.get_me()
    logger.info(f"✅ بات: @{bot_info.username}")
    
    webhook_url = f"https://warzoneir-1.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    logger.info("✅ وب‌هوک تنظیم شد")

async def create_app():
    await on_startup()
    app = web.Application()
    
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")
    
    app.router.add_get('/', health_check)
    return app

def main():
    logger.info("🎯 شروع راه‌اندازی بات...")
    app = asyncio.run(create_app())
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
