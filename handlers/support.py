from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import Database

db = Database()
support_router = Router()

class SupportState(StatesGroup):
    waiting_message = State()

@support_router.message(Command("support"))
async def support_start(message: Message, state: FSMContext):
    await message.answer(
        "📞 **پشتیبانی WarZone**\n\n"
        "لطفاً پیام خود را برای پشتیبانی ارسال کنید:\n"
        "(می‌توانید مشکل، پیشنهاد یا انتقاد خود را بنویسید)"
    )
    await state.set_state(SupportState.waiting_message)

@support_router.message(SupportState.waiting_message)
async def process_support_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or "بدون نام"
    support_text = message.text
    
    # اینجا می‌توانید پیام را به ادمین ارسال کنید
    # یا در دیتابیس ذخیره کنید
    
    await message.answer(
        "✅ **پیام شما دریافت شد!**\n\n"
        "از اینکه بازخورد خود را با ما در میان گذاشتید متشکریم.\n"
        "تیم پشتیبانی در اسرع وقت پاسخگو خواهد بود.\n\n"
        "⚔️ با قدرت به جنگ ادامه دهید!"
    )
    
    await state.clear()
