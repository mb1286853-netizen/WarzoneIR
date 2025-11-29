from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def shop_main_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🚀 موشک‌ها", callback_data="shop_missiles"),
        InlineKeyboardButton(text="🛩 جنگنده", callback_data="shop_fighters")
    )
    builder.row(
        InlineKeyboardButton(text="🛸 پهپاد", callback_data="shop_drones"),
        InlineKeyboardButton(text="🔧 پدافند", callback_data="shop_defense")
    )
    builder.row(
        InlineKeyboardButton(text="💎 آیتم‌ها", callback_data="shop_items"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")
    )
    
    return builder.as_markup()

def missiles_category_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎯 عادی", callback_data="normal_missiles"),
        InlineKeyboardButton(text="🚀 ویژه", callback_data="special_missiles")
    )
    builder.row(
        InlineKeyboardButton(text="☠️ آخرالزمانی", callback_data="doomsday_missiles"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="shop_main")
    )
    
    return builder.as_markup()

def normal_missiles_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="تیرباران - 400 ZP", callback_data="buy_tirbaran"),
        InlineKeyboardButton(text="رعدآسا - 700 ZP", callback_data="buy_raadasa")
    )
    builder.row(
        InlineKeyboardButton(text="تندباد - 1000 ZP", callback_data="buy_tondbad"),
        InlineKeyboardButton(text="زلزله - 1500 ZP", callback_data="buy_zelzele")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="shop_missiles")
    )
    
    return builder.as_markup()

def special_missiles_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="آتشفشان - 8,000 ZP", callback_data="buy_ateshfshan"),
        InlineKeyboardButton(text="توفان‌نو - 15,000 ZP", callback_data="buy_toofannoo")
    )
    builder.row(
        InlineKeyboardButton(text="خاموش‌کن - 20,000 ZP", callback_data="buy_khamoshkon"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="shop_missiles")
    )
    
    return builder.as_markup()

def doomsday_missiles_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="عقاب‌توفان - 30,000 ZP + 3 جم", callback_data="buy_oghabs"),
        InlineKeyboardButton(text="اژدهای‌آتش - 45,000 ZP + 5 جم", callback_data="buy_azhdaha")
    )
    builder.row(
        InlineKeyboardButton(text="فینیکس - 60,000 ZP + 8 جم", callback_data="buy_phoenix"),
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="shop_missiles")
    )
    
    return builder.as_markup()
