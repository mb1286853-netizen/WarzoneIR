from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.combo_menu import (
    combo_main_keyboard,
    create_combo_keyboard,
    attack_with_combo_keyboard
)
from database import Database

db = Database()
combo_router = Router()

class ComboCreation(StatesGroup):
    choosing_fighter = State()
    choosing_drone = State()
    choosing_missiles = State()

@combo_router.message(F.text == "🎯 ترکیب‌ها")
async def combo_main(message: Message):
    await message.answer(
        "⚔️ **سیستم ترکیب‌های حمله**\n\n"
        "می‌توانید ۳ ترکیب مختلف بسازید و با دستور سریع حمله کنید\n\n"
        "👇 گزینه مورد نظر را انتخاب کنید:",
        reply_markup=combo_main_keyboard()
    )

@combo_router.callback_query(F.data == "create_combo_1")
async def create_combo_1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ComboCreation.choosing_fighter)
    await state.update_data(combo_number=1)
    
    await callback.message.edit_text(
        "🛠 **ساخت ترکیب ۱**\n\n"
        "👇 جنگنده مورد نظر را انتخاب کنید:",
        reply_markup=create_combo_keyboard("fighter")
    )
