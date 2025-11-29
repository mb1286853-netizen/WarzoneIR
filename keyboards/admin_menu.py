from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="💰 انتقال ZP", callback_data="admin_transfer_coin"),
        InlineKeyboardButton(text="💎 انتقال جم", callback_data="admin_transfer_gem")
    )
    builder.row(
        InlineKeyboardButton(text="⭐ انتقال لول", callback_data="admin_transfer_level"),
        InlineKeyboardButton(text="🚀 انتقال موشک", callback_data="admin_transfer_missile")
    )
    builder.row(
        InlineKeyboardButton(text="📊 آمار کلی", callback_data="admin_stats"),
        InlineKeyboardButton(text="📢 پیام همگانی", callback_data="admin_broadcast")
    )
    builder.row(
        InlineKeyboardButton(text="👤 مدیریت کاربران", callback_data="admin_users"),
        InlineKeyboardButton(text="⚙️ تنظیمات", callback_data="admin_settings")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()
