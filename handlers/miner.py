from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.miner_menu import miner_keyboard
from database import Database
import time

db = Database()
miner_router = Router()

MINER_LEVELS = {
    1: {"production": 100, "upgrade_cost": 100},
    2: {"production": 200, "upgrade_cost": 200},
    3: {"production": 350, "upgrade_cost": 300},
    # ... تا سطح ۱۵
}

@miner_router.message(F.text == "⛏ ماینر")
async def miner_status(message: Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        return
    
    miner_level = user[10]  # miner_level
    miner_balance = user[11]  # miner_balance
    last_claim = user[12]  # last_miner_claim
    
    current_time = int(time.time())
    time_since_last_claim = current_time - last_claim if last_claim else 0
    max_balance = MINER_LEVELS[miner_level]["production"]
    
    # محاسبه موجودی فعلی
    if time_since_last_claim >= 10800:  # 3 ساعت
        current_balance = max_balance
    else:
        current_balance = min(miner_balance + (time_since_last_claim * max_balance // 10800), max_balance)
    
    await message.answer(
        f"⛏ **وضعیت ماینر**\n\n"
        f"📊 سطح: {miner_level}\n"
        f"💰 تولید: {MINER_LEVELS[miner_level]['production']} ZP/3ساعت\n"
        f"💎 موجودی قابل برداشت: {current_balance} ZP\n"
        f"🔼 هزینه ارتقا: {MINER_LEVELS[miner_level]['upgrade_cost']} ZP\n\n"
        f"💡 پس از ۳ ساعت تولید متوقف می‌شود",
        reply_markup=miner_keyboard(current_balance, miner_level)
    )
