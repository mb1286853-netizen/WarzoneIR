from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.admin_menu import admin_main_keyboard
from database import Database

db = Database()
admin_router = Router()

# لیست ادمین‌ها
ADMINS = [123456789]  # جایگزین کنید با آی‌دی عددی خودتان

class AdminTransfer(StatesGroup):
    waiting_user_id = State()
    waiting_amount = State()

def is_admin(user_id):
    return user_id in ADMINS

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ دسترسی denied!")
        return
    
    await message.answer(
        "👑 <b>پنل مدیریت WarZone</b>\n\n"
        "👇 گزینه مورد نظر را انتخاب کنید:",
        reply_markup=admin_main_keyboard(),
        parse_mode="HTML"
    )

@admin_router.callback_query(F.data == "admin_transfer_coin")
async def transfer_coin_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer(
        "💰 <b>انتقال ZP</b>\n\n"
        "لطفاً آی‌دی کاربر را وارد کنید:"
    )
    await state.set_state(AdminTransfer.waiting_user_id)

@admin_router.message(AdminTransfer.waiting_user_id)
async def process_user_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        await state.update_data(target_user=user_id)
        await message.answer("💰 مقدار ZP را وارد کنید:")
        await state.set_state(AdminTransfer.waiting_amount)
    except ValueError:
        await message.answer("❌ آی‌دی باید عددی باشد!")

@admin_router.message(AdminTransfer.waiting_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        data = await state.get_data()
        target_user = data['target_user']
        
        # انتقال سکه
        db.update_user_coin(target_user, amount)
        
        await message.answer(
            f"✅ <b>انتقال انجام شد</b>\n\n"
            f"👤 کاربر: {target_user}\n"
            f"💰 مقدار: {amount} ZP\n"
            f"🕰 زمان: {message.date.strftime('%Y-%m-%d %H:%M')}"
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ مقدار باید عددی باشد!")
