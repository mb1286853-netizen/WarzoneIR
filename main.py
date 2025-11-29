import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os

# تنظیمات
TOKEN = os.getenv("TOKEN")

async def main():
    print("🔧 شروع راه‌اندازی بات...")
    
    # ساخت بات
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # منوی ساده
    async def send_menu(chat_id):
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👤 پروفایل"), KeyboardButton(text="⚔️ حمله")],
                [KeyboardButton(text="🛒 فروشگاه"), KeyboardButton(text="⛏ ماینر")]
            ],
            resize_keyboard=True
        )
        
        await bot.send_message(
            chat_id,
            "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
            "✅ بات فعال و آماده!\n"
            "👇 از منو استفاده کنید:",
            reply_markup=keyboard
        )
    
    # هندلر استارت
    @dp.message(Command("start"))
    async def start_cmd(message: types.Message):
        print(f"🎯 کاربر {message.from_user.id} بات رو استارت کرد")
        await send_menu(message.chat.id)
    
    # هندلر منو
    @dp.message()
    async def menu_handler(message: types.Message):
        text = message.text
        user_id = message.from_user.id
        
        print(f"📱 کاربر {user_id}: {text}")
        
        if text == "👤 پروفایل":
            await message.answer(
                "👤 **پروفایل شما**\n\n"
                "⭐ سطح: ۱\n💰 ZP: ۱,۰۰۰\n💎 جم: ۰\n"
                "💪 قدرت: ۱۰۰\n🛡️ پدافند: سطح ۱"
            )
        
        elif text == "⚔️ حمله":
            await message.answer("⚔️ **سیستم حمله**\n\n🔜 به زودی فعال می‌شود")
        
        elif text == "🛒 فروشگاه":
            await message.answer("🛒 **فروشگاه**\n\n🔜 به زودی فعال می‌شود")
        
        elif text == "⛏ ماینر":
            await message.answer("⛏ **ماینر**\n\n🔜 به زودی فعال می‌شود")
        
        else:
            await send_menu(message.chat.id)
    
    # اطلاعات بات
    bot_info = await bot.get_me()
    print(f"✅ بات: @{bot_info.username}")
    print("🚀 بات فعال شد! منتظر پیام...")
    
    # شروع
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
