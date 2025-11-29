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

# تست ساخت Bot object
try:
    logger.info("🔄 در حال ساخت Bot object...")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.info("✅ Bot object ساخته شد")
except Exception as e:
    logger.error(f"❌ خطا در ساخت Bot: {str(e)}")
    logger.error(f"🔍 نوع خطا: {type(e).__name__}")
    
    # حالت fallback
    async def health_check(request):
        return web.Response(text=f"❌ Bot Creation Failed: {type(e).__name__}")
    
    app = web.Application()
    app.router.add_get('/', health_check)
    web.run_app(app, host='0.0.0.0', port=8000)
    exit()

dp = Dispatcher()
logger.info("✅ Dispatcher ساخته شد")

@dp.message(Command("start"))
async def start_command(message: Message):
    logger.info(f"🎯 START از: {message.from_user.id}")
    await message.answer("✅ بات فعال است!")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Server OK")

async def on_startup(app):
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
        logger.error(f"🔍 نوع خطا: {type(e).__name__}")

def main():
    dp.startup.register(on_startup)
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get('/', health_check)
    
    logger.info("🚀 سرور راه‌اندازی شد - منتظر وب‌هوک...")
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
