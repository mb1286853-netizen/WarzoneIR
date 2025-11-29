from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def miner_keyboard(balance, level):
    builder = InlineKeyboardBuilder()
    
    if balance > 0:
        builder.row(
            InlineKeyboardButton(text="💰 برداشت", callback_data="miner_claim")
        )
    
    if level < 15:
        builder.row(
            InlineKeyboardButton(text="🔼 ارتقا ماینر", callback_data="miner_upgrade")
        )
    
    builder.row(
        InlineKeyboardButton(text="📊 اطلاعات ماینر", callback_data="miner_info"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()

def confirm_upgrade_keyboard(cost):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text=f"✅ ارتقا بده ({cost} ZP)", callback_data="confirm_upgrade"),
        InlineKeyboardButton(text="❌ انصراف", callback_data="miner_main")
    )
    
    return builder.as_markup()
