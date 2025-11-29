import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logging.error("❌ Token not found!")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("🚀 WarZone Bot is working!")

if __name__ == "__main__":
    logging.info("✅ Bot starting...")
    dp.run_polling(bot)
