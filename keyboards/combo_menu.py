from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def combo_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🛠 ترکیب ۱", callback_data="create_combo_1"),
        InlineKeyboardButton(text="🛠 ترکیب ۲", callback_data="create_combo_2"),
        InlineKeyboardButton(text="🛠 ترکیب ۳", callback_data="create_combo_3")
    )
    builder.row(
        InlineKeyboardButton(text="📋 ترکیب‌های من", callback_data="my_combos"),
        InlineKeyboardButton(text="🎯 حمله با ترکیب", callback_data="attack_with_combo")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()

def create_combo_keyboard(step):
    builder = InlineKeyboardBuilder()
    
    if step == "fighter":
        builder.row(
            InlineKeyboardButton(text="شب‌پرواز - 5,000 ZP", callback_data="combo_fighter_shab"),
            InlineKeyboardButton(text="توفان‌ساز - 8,000 ZP", callback_data="combo_fighter_toofan")
        )
        builder.row(
            InlineKeyboardButton(text="آذرخش - 12,000 ZP", callback_data="combo_fighter_azderakhsh"),
            InlineKeyboardButton(text="شبح‌ساحل - 18,000 ZP", callback_data="combo_fighter_shabh")
        )
    
    elif step == "drone":
        builder.row(
            InlineKeyboardButton(text="زنبورک - 3,000 ZP", callback_data="combo_drone_zanboorak"),
            InlineKeyboardButton(text="سایفر - 5,000 ZP", callback_data="combo_drone_cipher")
        )
        builder.row(
            InlineKeyboardButton(text
