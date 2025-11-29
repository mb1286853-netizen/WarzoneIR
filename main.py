import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"🔑 توکن: {'وجود دارد' if TOKEN else 'وجود ندارد'}")

if not TOKEN:
    logger.error("❌ توکن پیدا نشد!")
    async def health_check(request):
        return web.Response(text="❌ TOKEN not found")
    
    app = web.Application()
    app.router.add_get('/', health_check)
    web.run_app(app, host='0.0.0.0', port=8000)
    exit()

# ساخت Bot و Dispatcher
try:
    logger.info("🔄 در حال ساخت Bot object...")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    logger.info("✅ Bot و Dispatcher ساخته شدند")
except Exception as e:
    logger.error(f"❌ خطا در ساخت Bot: {str(e)}")
    async def health_check(request):
        return web.Response(text=f"❌ Bot Error: {type(e).__name__}")
    app = web.Application()
    app.router.add_get('/', health_check)
    web.run_app(app, host='0.0.0.0', port=8000)
    exit()

@dp.message(Command("start"))
async def start_command(message: Message):
    logger.info(f"🎯 START از: {message.from_user.id}")
    await message.answer("🎯 **به WarZone خوش آمدید!**\n\nبات آنلاین و فعال است! ⚔️")

@dp.message()
async def echo_handler(message: Message):
    logger.info(f"📩 پیام: {message.text}")
    await message.answer("🤖 از /start استفاده کنید")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active! ⚔️")

async def on_startup():
    """تابع startup که قبل از راه‌اندازی سرور اجرا می‌شه"""
    logger.info("🔄 شروع تنظیم وب‌هوک...")
    try:
        # تست اتصال به تلگرام
        logger.info("🔗 تست اتصال به تلگرام...")
        bot_info = await bot.get_me()
        logger.info(f"✅ بات: @{bot_info.username} (ID: {bot_info.id})")
        
        # تنظیم وب‌هوک
        webhook_url = f"https://warzoneir-1.onrender.com/webhook"
        await bot.set_webhook(webhook_url)
        logger.info(f"✅ وب‌هوک تنظیم شد: {webhook_url}")
        
    except Exception as e:
        logger.error(f"❌ خطا در اتصال به تلگرام: {str(e)}")

async def create_app():
    """ساخت اپلیکیشن aiohttp"""
    await on_startup()  # اجرای دستی تابع startup
    
    app = web.Application()
    
    # ثبت وب‌هوک هندلر
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    
    # صفحه سلامت
    app.router.add_get('/', health_check)
    
    logger.info("🚀 اپلیکیشن ساخته شد")
    return app

def main():
    logger.info("🎯 شروع راه‌اندازی WarZone Bot...")
    
    # اجرای غیرهمزمان
    async def run_server():
        app = await create_app()
        return app
    
    # راه‌اندازی سرور
    app = asyncio.run(run_server())
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
