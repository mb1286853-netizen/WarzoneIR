from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.sabotage_menu import sabotage_main_keyboard, sabotage_types_keyboard
from database import Database
import random

db = Database()
sabotage_router = Router()

class SabotageState(StatesGroup):
    choosing_target = State()
    choosing_type = State()

SABOTAGE_TYPES = {
    "infiltrator": {
        "name": "خرابکار نفوذی",
        "cost": 500,
        "success_rate": 60,
        "effect": "کاهش ۳۰٪ پدافند دشمن"
    },
    "electronic": {
        "name": "خرابکار الکترونیکی", 
        "cost": 1200,
        "success_rate": 50,
        "effect": "غیرفعال کردن امنیت سایبری"
    },
    "informational": {
        "name": "خرابکار اطلاعاتی",
        "cost": 2000, 
        "success_rate": 40,
        "effect": "افزایش غارت تا ۷۵٪"
    }
}

@sabotage_router.message(F.text == "🕵️ خرابکاری")
async def sabotage_main(message: Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        return
    
    cyber_level = user[9]  # cyber_level
    
    await message.answer(
        f"🕵️ <b>سیستم خرابکاری</b>\n\n"
        f"🔒 <b>سطح امنیت سایبری شما:</b> {cyber_level}/5\n"
        f"💡 با ارتقای امنیت سایبری از خرابکاری در امان بمانید\n\n"
        f"👇 نوع خرابکاری را انتخاب کنید:",
        reply_markup=sabotage_main_keyboard()
    )

@sabotage_router.callback_query(F.data == "start_sabotage")
async def start_sabotage(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🎯 <b>شروع خرابکاری</b>\n\n"
        "لطفاً روی کاربر مورد نظر ریپلای کنید",
        reply_markup=sabotage_types_keyboard()
    )
    await state.set_state(SabotageState.choosing_target)
