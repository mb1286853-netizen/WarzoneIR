from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.attack_menu import attack_main_keyboard, single_attack_keyboard
from database import Database
import random
import time

db = Database()
attack_router = Router()

class SingleAttack(StatesGroup):
    choosing_target = State()
    choosing_missile = State()

@attack_router.message(F.text == "⚔️ حمله")
async def attack_main(message: Message):
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "👇 نوع حمله را انتخاب کنید:",
        reply_markup=attack_main_keyboard()
    )

@attack_router.callback_query(F.data == "single_attack")
async def single_attack_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🎯 **حمله تکی**\n\n"
        "لطفاً روی کاربر مورد نظر ریپلای کنید و دستور حمله را بزنید:\n"
        "مثال: <code>حمله تیرباران</code>"
    )
    await state.set_state(SingleAttack.choosing_target)

@attack_router.message(SingleAttack.choosing_target, F.reply_to_message)
async def process_single_attack(message: Message, state: FSMContext):
    target_user = message.reply_to_message.from_user
    command = message.text.lower()
    
    # استخراج نام موشک از دستور
    missile_name = command.replace("حمله", "").strip()
    
    # بررسی موجودی موشک
    user_missiles = db.get_user_missiles(message.from_user.id)
    if missile_name not in user_missiles or user_missiles[missile_name] == 0:
        await message.answer("❌ این موشک را ندارید!")
        return
    
    # محاسبه دمیج
    missile_damage = {
        "تیرباران": 60,
        "رعدآسا": 90,
        "تندباد": 120,
        "زلزله": 130
    }.get(missile_name, 50)
    
    # شانس حمله بحرانی
    is_critical = random.random() <= 0.15  # 15% شانس
    final_damage = missile_damage * 2 if is_critical else missile_damage
    
    # محاسبه غارت
    loot = random.randint(50, 200)
    if is_critical:
        loot *= 2
    
    # کاهش موجودی موشک
    db.update_missile_quantity(message.from_user.id, missile_name, -1)
    
    # افزودن غارت به کاربر
    db.update_user_coin(message.from_user.id, loot)
    
    # افزودن XP
    xp_gained = 10 * (2 if is_critical else 1)
    db.update_user_xp(message.from_user.id, xp_gained)
    
    # پیام به مهاجم
    attack_message = (
        f"🎯 <b>حمله {'بحرانی 🔥' if is_critical else 'موفق'}!</b>\n\n"
        f"⚔️ <b>مهاجم:</b> {message.from_user.first_name}\n"
        f"🛡️ <b>مدافع:</b> {target_user.first_name}\n"
        f"💥 <b>موشک:</b> {missile_name}\n\n"
        f"📊 <b>آمار حمله:</b>\n"
        f"• دمیج: {final_damage} {'(بحرانی)' if is_critical else ''}\n"
        f"• غارت: +{loot} ZP\n"
        f"• XP: +{xp_gained}\n\n"
        f"⏰ {time.strftime('%Y-%m-%d %H:%M')}"
    )
    
    await message.answer(attack_message)
    await state.clear()
