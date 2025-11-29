import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات بات
BOT_TOKEN = os.getenv("TOKEN")
ADMIN_IDS = [123456789]  # آی‌دی ادمین‌ها

# تنظیمات بازی
STARTING_COINS = 1000
STARTING_GEMS = 0
MAX_MINER_LEVEL = 15

# تنظیمات سرور
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
PORT = int(os.getenv("PORT", 8000))
