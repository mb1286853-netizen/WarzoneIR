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

# لاگ توکن برای دیباگ
logger.info(f"🔑 توکن در سیستم: {'وجود دارد' if TOKEN else 'وجود ندارد'}")

if not TOKEN:
    logger.error("❌ توکن پیدا نشد! لطفاً در رندر تنظیم کنید")
    async def health_check(request):
        return web.Response(text="❌ TOKEN not found in environment variables")
    
    app = web.Application()
    app.router.add_get('/', health_check)
    web.run_app(app, host='0.0.0.0', port=8000)

else:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: Message):
        user = message.from_user
        logger.info(f"🎯 دریافت /start از: {user.id}")
        await message.answer(
            "🎯 **به WarZone خوش آمدید!**\n\n"
            f"🆔 شناسه شما: {user.id}\n"
            "✅ بات آنلاین و فعال است!"
        )

    @dp.message()
    async def all_messages(message: Message):
        logger.info(f"📩 پیام: {message.text}")
        await message.answer("🤖 بات فعال است! از /start استفاده کنید")

    async def health_check(request):
        return web.Response(text="✅ WarZone Bot - Active! ⚔️")

    async def on_startup(app):
        webhook_url = f"https://warzoneir-1.onrender.com/webhook"
        try:
            await bot.set_webhook(webhook_url)
            logger.info(f"✅ وب‌هوک تنظیم شد")
            
            # تست اتصال بات
            bot_info = await bot.get_me()
            logger.info(f"🤖 بات: @{bot_info.username}")
            
        except Exception as e:
            logger.error(f"❌ خطا در تنظیم بات: {e}")

    def main():
        dp.startup.register(on_startup)
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
        app.router.add_get('/', health_check)
        
        logger.info("🚀 WarZone Bot راه‌اندازی شد...")
        web.run_app(app, host='0.0.0.0', port=8000)

    if __name__ == '__main__':
        main()
