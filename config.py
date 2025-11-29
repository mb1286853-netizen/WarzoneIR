import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات اصلی بات
BOT_TOKEN = os.getenv("TOKEN")
ADMIN_IDS = [7664487388]  # آی‌دی ادمین‌ها - جایگزین کنید

# تنظیمات بازی
STARTING_COINS = 1000
STARTING_GEMS = 0
MAX_MINER_LEVEL = 15
MAX_DEFENSE_LEVEL = 5
MAX_CYBER_LEVEL = 5

# تنظیمات موشک‌ها
MISSILE_PRICES = {
    "تیرباران": 400,
    "رعدآسا": 700,
    "تندباد": 1000,
    "زلزله": 1500,
    "آتشفشان": 8000,
    "توفان‌نو": 15000,
    "خاموش‌کن": 20000,
    "عقاب‌توفان": 30000,
    "اژدهای‌آتش": 45000,
    "فینیکس": 60000
}

MISSILE_GEM_COSTS = {
    "عقاب‌توفان": 3,
    "اژدهای‌آتش": 5,
    "فینیکس": 8
}

# تنظیمات جنگنده‌ها
FIGHTER_PRICES = {
    "شب‌پرواز": 5000,
    "توفان‌ساز": 8000,
    "آذرخش": 12000,
    "شبح‌ساحل": 18000
}

# تنظیمات پهپادها
DRONE_PRICES = {
    "زنبورک": 3000,
    "سایفر": 5000,
    "ریزپرنده": 8000
}

# تنظیمات جعبه‌ها
BOX_PRICES = {
    "bronze": 0,
    "silver": 5000,
    "gold": 2,
    "diamond": 5,
    "legendary": 15
}

# تنظیمات سرور
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
PORT = int(os.getenv("PORT", 8000))
