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

# تنظیم لاگ‌گیری
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

# هندلر اصلی
@dp.message(Command("start"))
async def start_command(message: Message):
    user = message.from_user
    logger.info(f"🎯 START از: {user.id} (@{user.username})")
    
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "🛠 *سیستم در حال توسعه است*\n\n"
        "🔹 /start - اطلاعات بات\n"
        "🔹 /profile - پروفایل\n"
        "🔹 /attack - حمله\n"
        "🔹 /shop - فروشگاه\n\n"
        "✅ بات آنلاین و فعال است!"
    )

@dp.message(Command("profile"))
async def profile_command(message: Message):
    logger.info(f"📊 PROFILE از: {message.from_user.id}")
    await message.answer(
        "👤 **پروفایل شما**\n\n"
        "⭐ سطح: ۱\n"
        "💰 ZP: ۱,۰۰۰\n" 
        "💎 جم: ۰\n"
        "💪 قدرت: ۱۰۰\n\n"
        "🔜 به زودی کامل می‌شود"
    )

@dp.message(Command("attack"))
async def attack_command(message: Message):
    logger.info(f"⚔️ ATTACK از: {message.from_user.id}")
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "🔸 حمله تکی\n"
        "🔸 حمله ترکیبی\n"
        "🔸 سیستم غارت\n\n"
        "🔜 به زودی فعال می‌شود"
    )

@dp.message(Command("shop"))
async def shop_command(message: Message):
    logger.info(f"🛒 SHOP از: {message.from_user.id}")
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 موشک‌ها\n"
        "🛩 جنگنده‌ها\n" 
        "🛸 پهپادها\n"
        "🔧 پدافند\n\n"
        "🔜 به زودی فعال می‌شود"
    )

@dp.message()
async def all_messages(message: Message):
    logger.info(f"📩 پیام عادی: '{message.text}' از: {message.from_user.id}")
    await message.answer(
        "🤖 از دستورات استفاده کنید:\n\n"
        "/start - اطلاعات بات\n"
        "/profile - پروفایل\n" 
        "/attack - حمله\n"
        "/shop - فروشگاه"
    )

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active! ⚔️")

async def on_startup():
    """تابع startup"""
    logger.info("🔄 شروع تنظیم وب‌هوک...")
    try:
        # تست اتصال به تلگرام
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
    await on_startup()
    
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
    
    async def run_server():
        app = await create_app()
        return app
    
    app = asyncio.run(run_server())
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
