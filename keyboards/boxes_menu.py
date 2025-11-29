from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def boxes_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📦 برنزی (رایگان)", callback_data="open_bronze_box"),
        InlineKeyboardButton(text="🥈 نقره‌ای (5,000 ZP)", callback_data="open_silver_box")
    )
    builder.row(
        InlineKeyboardButton(text="🥇 طلایی (2 جم)", callback_data="open_gold_box"),
        InlineKeyboardButton(text="💎 الماس (5 جم)", callback_data="open_diamond_box")
    )
    builder.row(
        InlineKeyboardButton(text="🌟 افسانه‌ای (15 جم)", callback_data="open_legendary_box"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()

def confirm_box_keyboard(box_type):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✅ بله، باز کن", callback_data=f"confirm_{box_type}"),
        InlineKeyboardButton(text="❌ انصراف", callback_data="boxes_main")
    )
    
    return builder.as_markup()
