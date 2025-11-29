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

# تنظیم لاگ‌گیری - فقط خطاهای مهم رو نشون بده
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# کاهش لاگ‌های aiogram
logging.getLogger('aiogram').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)

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
    
    # غیرفعال کردن بعضی middleware ها برای کاهش ارور
    dp["_aiogram_skip_updates"] = True
    
    logger.info("✅ Bot و Dispatcher ساخته شدند")
except Exception as e:
    logger.error(f"❌ خطا در ساخت Bot: {str(e)}")
    async def health_check(request):
        return web.Response(text=f"❌ Bot Error: {type(e).__name__}")
    app = web.Application()
    app.router.add_get('/', health_check)
    web.run_app(app, host='0.0.0.0', port=8000)
    exit()

# هندلر اصلی با مدیریت ارور
@dp.message(Command("start"))
async def start_command(message: Message):
    try:
        user = message.from_user
        logger.info(f"🎯 START از: {user.id} (@{user.username})")
        
        await message.answer(
            "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
            "🛠 *سیستم در حال توسعه است*\n\n"
            "🔹 /start - اطلاعات بات\n"
            "🔹 /profile - پروفایل\n"
            "🔹 /attack - حمله\n"
            "🔹 /shop - فروشگاه\n"
            "🔹 /miner - ماینر\n\n"
            "✅ بات آنلاین و فعال است!"
        )
    except Exception as e:
        logger.error(f"❌ خطا در start: {e}")

@dp.message(Command("profile"))
async def profile_command(message: Message):
    try:
        logger.info(f"📊 PROFILE از: {message.from_user.id}")
        await message.answer(
            "👤 **پروفایل شما**\n\n"
            "⭐ سطح: ۱\n"
            "💰 ZP: ۱,۰۰۰\n" 
            "💎 جم: ۰\n"
            "💪 قدرت: ۱۰۰\n"
            "🛡️ پدافند: سطح ۱\n\n"
            "🔜 به زودی کامل می‌شود"
        )
    except Exception as e:
        logger.error(f"❌ خطا در profile: {e}")

@dp.message(Command("attack"))
async def attack_command(message: Message):
    try:
        logger.info(f"⚔️ ATTACK از: {message.from_user.id}")
        await message.answer(
            "⚔️ **سیستم حمله**\n\n"
            "🎯 **حمله تکی**\n"
            "💥 **حمله ترکیبی**\n"
            "💰 **سیستم غارت**\n\n"
            "🔜 به زودی فعال می‌شود"
        )
    except Exception as e:
        logger.error(f"❌ خطا در attack: {e}")

@dp.message(Command("shop"))
async def shop_command(message: Message):
    try:
        logger.info(f"🛒 SHOP از: {message.from_user.id}")
        await message.answer(
            "🛒 **فروشگاه WarZone**\n\n"
            "🚀 موشک‌ها\n"
            "🛩 جنگنده‌ها\n" 
            "🛸 پهپادها\n"
            "🔧 پدافند\n"
            "💎 آیتم‌های ویژه\n\n"
            "🔜 به زودی فعال می‌شود"
        )
    except Exception as e:
        logger.error(f"❌ خطا در shop: {e}")

@dp.message(Command("miner"))
async def miner_command(message: Message):
    try:
        logger.info(f"⛏️ MINER از: {message.from_user.id}")
        await message.answer(
            "⛏️ **سیستم ماینر**\n\n"
            "💰 تولید: ۱۰۰ ZP/۳ساعت\n"
            "📊 سطح: ۱\n"
            "💎 موجودی: ۰ ZP\n\n"
            "🔜 به زودی فعال می‌شود"
        )
    except Exception as e:
        logger.error(f"❌ خطا در miner: {e}")

@dp.message()
async def all_messages(message: Message):
    try:
        logger.info(f"📩 پیام: '{message.text}' از: {message.from_user.id}")
        await message.answer(
            "🤖 **دستورات موجود:**\n\n"
            "/start - اطلاعات بات\n"
            "/profile - پروفایل\n" 
            "/attack - حمله\n"
            "/shop - فروشگاه\n"
            "/miner - ماینر"
        )
    except Exception as e:
        logger.error(f"❌ خطا در پردازش پیام: {e}")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active! ⚔️")

async def on_startup():
    """تابع startup"""
    logger.info("🔄 شروع تنظیم وب‌هوک...")
    try:
        bot_info = await bot.get_me()
        logger.info(f"✅ بات: @{bot_info.username} (ID: {bot_info.id})")
        
        webhook_url = f"https://warzoneir-1.onrender.com/webhook"
        await bot.set_webhook(webhook_url)
        logger.info(f"✅ وب‌هوک تنظیم شد")
        
    except Exception as e:
        logger.error(f"❌ خطا در startup: {str(e)}")

async def create_app():
    """ساخت اپلیکیشن aiohttp"""
    await on_startup()
    
    app = web.Application()
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    
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
