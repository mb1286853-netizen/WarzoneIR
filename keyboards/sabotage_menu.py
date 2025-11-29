from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def sabotage_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎯 شروع خرابکاری", callback_data="start_sabotage"),
        InlineKeyboardButton(text="📊 تیم خرابکاری", callback_data="sabotage_team")
    )
    builder.row(
        InlineKeyboardButton(text="🔒 امنیت سایبری", callback_data="cyber_defense"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()

def sabotage_types_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🕵️ نفوذی - 500 ZP", callback_data="sabotage_infiltrator"),
        InlineKeyboardButton(text="💻 الکترونیکی - 1,200 ZP", callback_data="sabotage_electronic")
    )
    builder.row(
        InlineKeyboardButton(text="📡 اطلاعاتی - 2,000 ZP", callback_data="sabotage_informational"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="sabotage_main")
    )
    
    return builder.as_markup()

def confirm_sabotage_keyboard(sabotage_type, cost):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=f"✅ تأیید ({cost} ZP)", callback_data=f"confirm_{sabotage_type}"),
        InlineKeyboardButton(text="❌ انصراف", callback_data="sabotage_main")
    )
    
    return builder.as_markup()
