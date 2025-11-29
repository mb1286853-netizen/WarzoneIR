from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="⚔️ حمله"),
        KeyboardButton(text="🛒 فروشگاه")
    )
    builder.row(
        KeyboardButton(text="👤 پروفایل"),
        KeyboardButton(text="🛡️ دفاع")
    )
    builder.row(
        KeyboardButton(text="📦 جعبه"),
        KeyboardButton(text="⛏ ماینر")
    )
    builder.row(
        KeyboardButton(text="🕵️ خرابکاری"),
        KeyboardButton(text="🎯 ترکیب‌ها")
    )
    
    return builder.as_markup(resize_keyboard=True)
