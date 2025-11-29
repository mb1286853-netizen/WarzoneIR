from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.shop_menu import (
    shop_main_keyboard, 
    missiles_category_keyboard,
    normal_missiles_keyboard,
    special_missiles_keyboard,
    doomsday_missiles_keyboard
)
from database import Database

db = Database()
shop_router = Router()

class MissilePurchase(StatesGroup):
    choosing_missile = State()
    entering_quantity = State()

@shop_router.message(F.text == "🛒 فروشگاه")
async def shop_main(message: Message):
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "👇 دسته مورد نظر را انتخاب کنید:",
        reply_markup=shop_main_keyboard()
    )

@shop_router.callback_query(F.data == "shop_missiles")
async def missiles_category(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚀 **موشک‌ها**\n\n"
        "👇 نوع موشک مورد نظر را انتخاب کنید:",
        reply_markup=missiles_category_keyboard()
    )

@shop_router.callback_query(F.data == "normal_missiles")
async def normal_missiles(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 **موشک‌های عادی**\n\n"
        "موشک‌های پایه با محدودیت لول",
        reply_markup=normal_missiles_keyboard()
    )
