from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def attack_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎯 حمله تکی", callback_data="single_attack"),
        InlineKeyboardButton(text="💥 حمله ترکیبی", callback_data="combo_attack")
    )
    builder.row(
        InlineKeyboardButton(text="📊 تاریخچه حملات", callback_data="attack_history"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()

def single_attack_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="تیرباران 🎯", callback_data="attack_tirbaran"),
        InlineKeyboardButton(text="رعدآسا ⚡", callback_data="attack_raadasa")
    )
    builder.row(
        InlineKeyboardButton(text="تندباد 🌪️", callback_data="attack_tondbad"),
        InlineKeyboardButton(text="زلزله 🌋", callback_data="attack_zelzele")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="attack_main")
    )
    
    return builder.as_markup()
