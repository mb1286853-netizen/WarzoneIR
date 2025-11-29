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

# تنظیمات asyncio برای رندر
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

logging.basicConfig(level=logging.DEBUG)  # تغییر به DEBUG برای لاگ کامل
logger = logging.getLogger(__name__)

if not TOKEN:
    logger.error("❌ توکن پیدا نشد!")
    exit()

logger.info("🔄 ایجاد Bot instance...")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 پروفایل"), KeyboardButton(text="⚔️ حمله")],
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user = message.from_user
    logger.info(f"🎯 دریافت /start از کاربر: {user.id} (@{user.username})")
    
    try:
        logger.info("🔄 در حال ارسال پاسخ...")
        response = await message.answer(
            "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
            "✅ بات فعال است!\n"
            "👇 از منو استفاده کنید:",
            reply_markup=main_menu()
        )
        logger.info(f"✅ پاسخ ارسال شد! Message ID: {response.message_id}")
        
    except Exception as e:
        logger.error(f"❌ خطا در ارسال پاسخ: {e}")

@dp.message()
async def all_messages(message: Message):
    user = message.from_user
    logger.info(f"📩 دریافت پیام: '{message.text}' از: {user.id}")
    
    try:
        response = await message.answer(
            f"🤖 بات جواب میده!\nپیام شما: {message.text}",
            reply_markup=main_menu()
        )
        logger.info(f"✅ پاسخ ارسال شد: {response.message_id}")
        
    except Exception as e:
        logger.error(f"❌ خطا در ارسال پاسخ: {e}")

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active! ⚔️")

async def on_startup():
    try:
        logger.info("🔗 تست اتصال به تلگرام...")
        bot_info = await bot.get_me()
        logger.info(f"✅ بات: @{bot_info.username} (ID: {bot_info.id})")
        
        webhook_url = f"https://warzoneir-1.onrender.com/webhook"
        logger.info(f"🔄 تنظیم وب‌هوک: {webhook_url}")
        await bot.set_webhook(webhook_url)
        logger.info("✅ وب‌هوک تنظیم شد")
        
    except Exception as e:
        logger.error(f"❌ خطا در startup: {e}")

async def create_app():
    await on_startup()
    app = web.Application()
    
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")
    
    app.router.add_get('/', health_check)
    logger.info("🚀 اپلیکیشن ساخته شد")
    return app

def main():
    logger.info("🎯 شروع راه‌اندازی...")
    
    # ایجاد event loop جدید
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        app = loop.run_until_complete(create_app())
        logger.info("🌐 شروع سرور وب...")
        web.run_app(app, host='0.0.0.0', port=8000)
    except Exception as e:
        logger.error(f"❌ خطا در main: {e}")
    finally:
        loop.close()

if __name__ == '__main__':
    main()
