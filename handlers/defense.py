from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.defense_menu import defense_main_keyboard, upgrade_defense_keyboard
from database import Database

db = Database()
defense_router = Router()

DEFENSE_LEVELS = {
    1: {"name": "سپر-۹۵", "cost": 1000, "block_chance": 20},
    2: {"name": "سدیفاکتور", "cost": 2500, "block_chance": 35},
    3: {"name": "توربوشیلد", "cost": 5000, "block_chance": 50},
    4: {"name": "لایه نوری", "cost": 10000, "block_chance": 70},
    5: {"name": "پدافند افسانه‌ای", "cost": 20000, "block_chance": 90}
}

@defense_router.message(F.text == "🛡️ دفاع")
async def defense_main(message: Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        return
    
    defense_level = user[8]  # defense_level
    current_defense = DEFENSE_LEVELS.get(defense_level, DEFENSE_LEVELS[1])
    
    await message.answer(
        f"🛡️ <b>سیستم دفاع</b>\n\n"
        f"🛡️ <b>پدافند فعلی:</b> {current_defense['name']}\n"
        f"🎯 <b>شانس بلاک:</b> {current_defense['block_chance']}%\n"
        f"📊 <b>سطح:</b> {defense_level}/5\n\n"
        f"💡 پدافند باعث کاهش دمیج حملات می‌شود",
        reply_markup=defense_main_keyboard(defense_level)
    )

@defense_router.callback_query(F.data == "upgrade_defense")
async def upgrade_defense(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        return
    
    current_level = user[8]
    
    if current_level >= 5:
        await callback.answer("✅ شما حداکثر سطح پدافند را دارید!", show_alert=True)
        return
    
    next_level = current_level + 1
    upgrade_cost = DEFENSE_LEVELS[next_level]["cost"]
    user_coins = user[6]  # zone_coin
    
    if user_coins < upgrade_cost:
        await callback.answer(f"❌ موجودی ناکافی! نیاز: {upgrade_cost} ZP", show_alert=True)
        return
    
    # کسر هزینه و ارتقا
    db.update_user_coin(user_id, -upgrade_cost)
    db.update_user_defense_level(user_id, next_level)
    
    await callback.message.edit_text(
        f"🎉 <b>پدافند ارتقا یافت!</b>\n\n"
        f"🛡️ <b>پدافند جدید:</b> {DEFENSE_LEVELS[next_level]['name']}\n"
        f"🎯 <b>شانس بلاک:</b> {DEFENSE_LEVELS[next_level]['block_chance']}%\n"
        f"💰 <b>هزینه پرداخت‌شده:</b> {upgrade_cost} ZP\n\n"
        f"✅ امنیت پایگاه شما افزایش یافت"
    )
