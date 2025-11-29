from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.main_menu import main_menu_keyboard
from database import Database

db = Database()
start_router = Router()

@start_router.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    # ایجاد کاربر در دیتابیس
    db.create_user(user_id, username)
    
    await message.answer(
        "🎯 **به WarZone خوش آمدید!**\n\n"
        "⚔️ یک بازی استراتژیک با سیستم حمله و دفاع پیشرفته\n\n"
        "🔸 سیستم حملات تکی و ترکیبی\n"
        "🔸 جنگنده‌ها و موشک‌های متنوع\n"
        "🔸 سیستم ماینر و اقتصاد\n"
        "🔸 پدافند و خرابکاری\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu_keyboard()
    )
