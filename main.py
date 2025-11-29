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
if not TOKEN:
    raise ValueError("❌ توکن بات پیدا نشد!")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# هندلرهای اصلی
@dp.message(Command("start"))
async def start_command(message: Message):
    logger.info(f"📩 دریافت /start از کاربر: {message.from_user.id}")
    await message.answer(
        "🎯 **به WarZone خوش آمدید!**\n\n"
        "⚔️ یک بازی استراتژیک با سیستم حمله و دفاع پیشرفته\n\n"
        "✅ بات آنلاین و آماده است!\n"
        "🔜 به زودی قابلیت‌ها اضافه می‌شوند"
    )

@dp.message(Command("profile"))
async def profile_command(message: Message):
    logger.info(f"📩 دریافت /profile از کاربر: {message.from_user.id}")
    await message.answer(
        "👤 **پروفایل شما**\n\n"
        "⭐ سطح: ۱\n💰 ZP: ۱,۰۰۰\n💎 جم: ۰\n💪 قدرت: ۱۰۰\n\n"
        "🔜 سیستم پروفایل به زودی کامل می‌شود"
    )

# هندلر برای همه پیام‌ها
@dp.message()
async def echo_message(message: Message):
    logger.info(f"📩 دریافت پیام: {message.text} از {message.from_user.id}")
    await message.answer("🤖 بات فعال است! از /start استفاده کنید")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active and Ready! ⚔️")

async def on_startup(app):
    webhook_url = f"https://warzoneir-1.onrender.com/webhook"
    try:
        await bot.set_webhook(webhook_url)
        logger.info(f"✅ وب‌هوک تنظیم شد: {webhook_url}")
        
        # اطلاعات بات رو چک کنید
        bot_info = await bot.get_me()
        logger.info(f"🤖 بات: {bot_info.username} - {bot_info.first_name}")
    except Exception as e:
        logger.error(f"❌ خطا در تنظیم وب‌هوک: {e}")

def main():
    dp.startup.register(on_startup)
    
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get('/', health_check)
    
    logger.info("🚀 WarZone Bot شروع به کار کرد!")
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
