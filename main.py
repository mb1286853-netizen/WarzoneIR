import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text
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
    exit()

try:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    logger.info("✅ Bot و Dispatcher ساخته شدند")
except Exception as e:
    logger.error(f"❌ خطا در ساخت Bot: {e}")
    exit()

# ساخت منوی دکمه‌ای
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚔️ حمله"), KeyboardButton(text="👤 پروفایل")],
            [KeyboardButton(text="🛒 فروشگاه"), KeyboardButton(text="⛏ ماینر")],
            [KeyboardButton(text="📦 جعبه"), KeyboardButton(text="🛡 دفاع")],
            [KeyboardButton(text="🕵️ خرابکاری"), KeyboardButton(text="🎯 ترکیب‌ها")]
        ],
        resize_keyboard=True,
        input_field_placeholder="👇 از منو انتخاب کنید"
    )
    return keyboard

@dp.message(Command("start"))
async def start_command(message: Message):
    logger.info(f"🎯 شروع از کاربر: {message.from_user.id}")
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )

@dp.message(Text(text="👤 پروفایل"))
async def profile_menu(message: Message):
    logger.info(f"📊 پروفایل از: {message.from_user.id}")
    await message.answer(
        "👤 **پروفایل شما**\n\n"
        "⭐ سطح: ۱\n"
        "💰 ZP: ۱,۰۰۰\n" 
        "💎 جم: ۰\n"
        "💪 قدرت: ۱۰۰\n"
        "🛡️ پدافند: سطح ۱\n\n"
        "📈 برای پیشرفت از حمله استفاده کنید!",
        reply_markup=main_menu()
    )

@dp.message(Text(text="⚔️ حمله"))
async def attack_menu(message: Message):
    logger.info(f"⚔️ حمله از: {message.from_user.id}")
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "🎯 **حمله تکی** - استفاده از یک موشک\n"
        "💥 **حمله ترکیبی** - ترکیب جنگنده و موشک\n"
        "💰 **سیستم غارت** - کسب ZP از حمله\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(Text(text="🛒 فروشگاه"))
async def shop_menu(message: Message):
    logger.info(f"🛒 فروشگاه از: {message.from_user.id}")
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 **موشک‌ها** - از عادی تا آخرالزمانی\n"
        "🛩 **جنگنده‌ها** - افزایش قدرت حمله\n" 
        "🛸 **پهپادها** - حمله هوایی\n"
        "🔧 **پدافند** - حفاظت از پایگاه\n"
        "💎 **آیتم‌ها** - موارد ویژه\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(Text(text="⛏ ماینر"))
async def miner_menu(message: Message):
    logger.info(f"⛏️ ماینر از: {message.from_user.id}")
    await message.answer(
        "⛏️ **سیستم ماینر**\n\n"
        "💰 تولید: ۱۰۰ ZP/۳ساعت\n"
        "📊 سطح: ۱\n"
        "💎 موجودی: ۰ ZP\n"
        "🔼 ارتقا: ۱۰۰ ZP\n\n"
        "⏰ هر ۳ ساعت یکبار برداشت کنید",
        reply_markup=main_menu()
    )

@dp.message(Text(text="📦 جعبه"))
async def boxes_menu(message: Message):
    logger.info(f"📦 جعبه از: {message.from_user.id}")
    await message.answer(
        "📦 **جعبه‌های شانس**\n\n"
        "📦 برنزی - رایگان (۲۴h)\n"
        "🥈 نقره‌ای - ۵,۰۰۰ ZP\n"
        "🥇 طلایی - ۲ جم\n"
        "💎 الماس - ۵ جم\n"
        "🌟 افسانه‌ای - ۱۵ جم\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(Text(text="🛡 دفاع"))
async def defense_menu(message: Message):
    logger.info(f"🛡 دفاع از: {message.from_user.id}")
    await message.answer(
        "🛡 **سیستم دفاع**\n\n"
        "🔒 **پدافند** - کاهش دمیج حملات\n"
        "🛡 **امنیت سایبری** - جلوگیری از خرابکاری\n"
        "📊 **وضعیت دفاع** - مشاهده آمادگی\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(Text(text="🕵️ خرابکاری"))
async def sabotage_menu(message: Message):
    logger.info(f"🕵️ خرابکاری از: {message.from_user.id}")
    await message.answer(
        "🕵️ **سیستم خرابکاری**\n\n"
        "🕵️ **نفوذی** - کاهش پدافند دشمن\n"
        "💻 **الکترونیکی** - غیرفعال کردن سیستم\n"
        "📡 **اطلاعاتی** - افزایش غارت\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message(Text(text="🎯 ترکیب‌ها"))
async def combo_menu(message: Message):
    logger.info(f"🎯 ترکیب‌ها از: {message.from_user.id}")
    await message.answer(
        "🎯 **ترکیب‌های حمله**\n\n"
        "🛠 **ترکیب ۱** - حمله سریع\n"
        "🛠 **ترکیب ۲** - حمله سنگین\n"
        "🛠 **ترکیب ۳** - حمله ویژه\n\n"
        "🔜 به زودی فعال می‌شود",
        reply_markup=main_menu()
    )

@dp.message()
async def all_messages(message: Message):
    logger.info(f"📩 پیام: '{message.text}'")
    await message.answer(
        "🤖 لطفاً از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )

async def health_check(request):
    return web.Response(text="✅ WarZone Bot - Active! ⚔️")

async def on_startup():
    try:
        bot_info = await bot.get_me()
        logger.info(f"✅ بات: @{bot_info.username}")
        
        webhook_url = f"https://warzoneir-1.onrender.com/webhook"
        await bot.set_webhook(webhook_url)
        logger.info(f"✅ وب‌هوک تنظیم شد")
        
    except Exception as e:
        logger.error(f"❌ خطا: {e}")

async def create_app():
    await on_startup()
    app = web.Application()
    
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")
    
    app.router.add_get('/', health_check)
    logger.info("🚀 اپلیکیشن با منوی دکمه‌ای آماده")
    return app

def main():
    logger.info("🎯 راه‌اندازی بات با منوی دکمه‌ای...")
    app = asyncio.run(create_app())
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
