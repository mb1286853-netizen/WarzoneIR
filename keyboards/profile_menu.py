from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def profile_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📊 آمار دقیق", callback_data="profile_stats"),
        InlineKeyboardButton(text="🎖 لیگ من", callback_data="profile_league")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 دستاوردها", callback_data="profile_achievements"),
        InlineKeyboardButton(text="📈 نمودار پیشرفت", callback_data="profile_chart")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()
