from aiogram import Bot, Dispatcher, types
import asyncio
import os

TOKEN = os.getenv("TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    @dp.message()
    async def echo(message: types.Message):
        await message.answer("🤖 بات جواب میده!")
        print("✅ پاسخ ارسال شد")
    
    print("🚀 بات شروع شد...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
