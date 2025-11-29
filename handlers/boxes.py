from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.boxes_menu import boxes_main_keyboard
from database import Database
import random
import time

db = Database()
boxes_router = Router()

BOX_REWARDS = {
    "bronze": {
        "name": "📦 جعبه برنزی",
        "price": 0,
        "cooldown": 86400,
        "rewards": [
            {"type": "coin", "min": 50, "max": 150, "chance": 70},
            {"type": "missile", "name": "تیرباران", "chance": 20},
            {"type": "boost", "name": "XP کوچک", "chance": 10}
        ]
    },
    "silver": {
        "name": "🥈 جعبه نقره‌ای",
        "price": 5000,
        "rewards": [
            {"type": "coin", "min": 300, "max": 800, "chance": 50},
            {"type": "missile", "name": "رعدآسا", "chance": 25},
            {"type": "boost", "name": "حمله متوسط", "chance": 15},
            {"type": "missile", "name": "تندباد", "chance": 10}
        ]
    }
}

@boxes_router.message(F.text == "📦 جعبه")
async def boxes_main(message: Message):
    await message.answer(
        "🎁 **سیستم جعبه‌های شانس**\n\n"
        "👇 جعبه مورد نظر را انتخاب کنید:",
        reply_markup=boxes_main_keyboard()
    )

@boxes_router.callback_query(F.data == "open_bronze_box")
async def open_bronze_box(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    
    # بررسی خنک‌کاری
    last_open = user[13] if user else 0  # last_bronze_box
    current_time = int(time.time())
    
    if last_open and (current_time - last_open) < 86400:
        remaining = 86400 - (current_time - last_open)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        
        await callback.answer(
            f"⏰ جعبه برنزی قابل استفاده نیست! {hours} ساعت و {minutes} دقیقه باقی مانده",
            show_alert=True
        )
        return
    
    # انتخاب جایزه
    reward = random.choices(
        BOX_REWARDS["bronze"]["rewards"],
        weights=[r["chance"] for r in BOX_REWARDS["bronze"]["rewards"]]
    )[0]
    
    # اعطای جایزه
    if reward["type"] == "coin":
        amount = random.randint(reward["min"], reward["max"])
        db.update_user_coin(user_id, amount)
        reward_text = f"💰 {amount} ZP"
    elif reward["type"] == "missile":
        db.add_missile(user_id, reward["name"], 1)
        reward_text = f"🚀 ۱ عدد {reward['name']}"
    else:
        reward_text = f"⭐ {reward['name']}"
    
    # بروزرسانی زمان آخرین استفاده
    db.update_user_bronze_box_time(user_id, current_time)
    
    await callback.message.answer(
        f"🎉 {BOX_REWARDS['bronze']['name']} باز شد!\n\n"
        f"🎁 <b>جایزه شما:</b>\n"
        f"{reward_text}\n\n"
        f"⏰ جعبه برنزی بعدی: فردا این ساعت"
    )
