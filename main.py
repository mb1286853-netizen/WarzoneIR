import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ توکن بات پیدا نشد!")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ایمپورت هندلرها
try:
    from handlers.start import start_router
    from handlers.profile import profile_router
    from handlers.attack import attack_router
    logger.info("✅ هندلرها ایمپورت شدند")
except ImportError as e:
    logger.error(f"❌ خطا در ایمپورت: {e}")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active and Ready! ⚔️")

async def on_startup(app):
    webhook_url = f"https://warzoneir-1.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    logger.info(f"✅ وب‌هوک تنظیم شد: {webhook_url}")

def main():
    # ثبت هندلرها
    try:
        dp.include_router(start_router)
        dp.include_router(profile_router)
        dp.include_router(attack_router)
    except NameError:
        logger.warning("⚠️ برخی هندلرها موجود نیستند")
    
    dp.startup.register(on_startup)
    
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get('/', health_check)
    
    logger.info("🚀 WarZone Bot شروع به کار کرد!")
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
