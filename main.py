import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import sqlite3
import random
import os

print("🚀 شروع بات WarZone...")

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ توکن پیدا نشد!")
    exit()

# ساخت بات
bot = Bot(token=TOKEN)
dp = Dispatcher()

# دیتابیس پیشرفته
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('warzone.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # کاربران
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                zp INTEGER DEFAULT 1000,
                gem INTEGER DEFAULT 0,
                power INTEGER DEFAULT 100,
                defense_level INTEGER DEFAULT 1,
                cyber_level INTEGER DEFAULT 1,
                miner_level INTEGER DEFAULT 1,
                miner_balance INTEGER DEFAULT 0,
                last_miner_claim INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # موشک‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missiles (
                user_id INTEGER,
                missile_type TEXT,
                quantity INTEGER DEFAULT 0
            )
        ''')
        
        # جنگنده‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fighters (
                user_id INTEGER,
                fighter_type TEXT,
                equipped BOOLEAN DEFAULT FALSE
            )
        ''')
        
        self.conn.commit()

db = Database()

# سیستم کاربر
def get_user(user_id):
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        db.conn.commit()
        return get_user(user_id)
    return user

def update_user_zp(user_id, amount):
    cursor = db.conn.cursor()
    cursor.execute('UPDATE users SET zp = zp + ? WHERE user_id = ?', (amount, user_id))
    db.conn.commit()

def update_user_xp(user_id, amount):
    cursor = db.conn.cursor()
    cursor.execute('UPDATE users SET xp = xp + ? WHERE user_id = ?', (amount, user_id))
    
    # بررسی ارتقا سطح
    user = get_user(user_id)
    xp_needed = user[2] * 100  # سطح × ۱۰۰
    if user[3] >= xp_needed:
        cursor.execute('UPDATE users SET level = level + 1, xp = xp - ? WHERE user_id = ?', 
                      (xp_needed, user_id))
        db.conn.commit()
        return True  # سطح ارتقا یافت
    db.conn.commit()
    return False

def add_missile(user_id, missile_type, quantity=1):
    cursor = db.conn.cursor()
    cursor.execute('SELECT quantity FROM missiles WHERE user_id = ? AND missile_type = ?', 
                  (user_id, missile_type))
    result = cursor.fetchone()
    
    if result:
        cursor.execute('UPDATE missiles SET quantity = quantity + ? WHERE user_id = ? AND missile_type = ?', 
                      (quantity, user_id, missile_type))
    else:
        cursor.execute('INSERT INTO missiles (user_id, missile_type, quantity) VALUES (?, ?, ?)', 
                      (user_id, missile_type, quantity))
    db.conn.commit()

# منوی اصلی
def main_menu():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👤 پروفایل"), types.KeyboardButton(text="⚔️ حمله")],
            [types.KeyboardButton(text="🛒 فروشگاه"), types.KeyboardButton(text="⛏ ماینر")],
            [types.KeyboardButton(text="📦 جعبه"), types.KeyboardButton(text="🛡 دفاع")],
            [types.KeyboardButton(text="🕵️ خرابکاری"), types.KeyboardButton(text="🎯 ترکیب‌ها")]
        ],
        resize_keyboard=True
    )

# قیمت‌ها
MISSILE_PRICES = {
    "سومار": 500,
    "زلزله": 1000,
    "آتشفشان": 2000,
    "شهاب": 5000
}

FIGHTER_PRICES = {
    "شب‌پرواز": 5000,
    "توفان‌ساز": 8000,
    "آذرخش": 12000
}

# هندلرها
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(
        "🎯 **به WarZone خوش آمدید!** ⚔️\n\n"
        "✅ سیستم اقتصادی فعال شد!\n"
        f"💰 موجودی اولیه: {user[4]:,} ZP\n\n"
        "👇 از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )
    print(f"✅ کاربر {message.from_user.id} استارت زد")

@dp.message(lambda message: message.text == "👤 پروفایل")
async def profile_handler(message: types.Message):
    user = get_user(message.from_user.id)
    
    # محاسبه XP مورد نیاز
    xp_needed = user[2] * 100
    
    await message.answer(
        f"👤 **پروفایل شما**\n\n"
        f"⭐ سطح: {user[2]}\n"
        f"📊 XP: {user[3]}/{xp_needed}\n"
        f"💰 ZP: {user[4]:,}\n"
        f"💎 جم: {user[5]}\n"
        f"💪 قدرت: {user[6]}\n"
        f"🛡️ پدافند: سطح {user[7]}\n"
        f"🔒 امنیت: سطح {user[8]}\n"
        f"⛏️ ماینر: سطح {user[9]}",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "⚔️ حمله")
async def attack_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🎯 حمله تکی"), types.KeyboardButton(text="💥 حمله ترکیبی")],
            [types.KeyboardButton(text="🔙 منوی اصلی")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "⚔️ **سیستم حمله**\n\n"
        "🎯 **حمله تکی** - استفاده از یک موشک\n"
        "💥 **حمله ترکیبی** - ترکیب جنگنده و موشک\n"
        "💰 **جایزه**: XP + ZP\n\n"
        "👇 نوع حمله را انتخاب کنید:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "🎯 حمله تکی")
async def single_attack_handler(message: types.Message):
    user = get_user(message.from_user.id)
    
    # شانس حمله بحرانی
    is_critical = random.random() < 0.15  # 15% شانس
    base_reward = 50
    reward = base_reward * 2 if is_critical else base_reward
    
    # اعطای جایزه
    update_user_zp(message.from_user.id, reward)
    level_up = update_user_xp(message.from_user.id, 10)
    
    critical_text = " 🔥**بحرانی**" if is_critical else ""
    
    response = f"⚔️ **حمله موفق{critical_text}!**\n\n"
    response += f"💰 **جایزه**: {reward} ZP\n"
    response += f"⭐ **XP**: +۱۰\n"
    
    if level_up:
        response += f"🎉 **سطح شما ارتقا یافت!** (سطح {get_user(message.from_user.id)[2]})\n"
    
    response += f"\n💎 **موجودی جدید**: {user[4] + reward:,} ZP"
    
    await message.answer(response, reply_markup=main_menu())

@dp.message(lambda message: message.text == "🛒 فروشگاه")
async def shop_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🚀 موشک‌ها"), types.KeyboardButton(text="🛩 جنگنده‌ها")],
            [types.KeyboardButton(text="🔙 منوی اصلی")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        "🚀 **موشک‌ها** - قدرت حمله\n"
        "🛩 **جنگنده‌ها** - افزایش قدرت\n"
        "🛸 **پهپادها** - حمله هوایی\n\n"
        "👇 دسته مورد نظر را انتخاب کنید:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "🚀 موشک‌ها")
async def missiles_shop_handler(message: types.Message):
    user = get_user(message.from_user.id)
    
    missiles_text = "🚀 **موشک‌های موجود:**\n\n"
    for missile, price in MISSILE_PRICES.items():
        missiles_text += f"• {missile} - {price:,} ZP\n"
    
    missiles_text += f"\n💰 **موجودی شما**: {user[4]:,} ZP"
    missiles_text += "\n\nبرای خرید ریپلای کنید: <code>خرید موشک نامموشک</code>"
    
    await message.answer(missiles_text, reply_markup=main_menu())

@dp.message(lambda message: message.text == "⛏ ماینر")
async def miner_handler(message: types.Message):
    user = get_user(message.from_user.id)
    miner_income = user[9] * 100  # سطح × ۱۰۰
    
    await message.answer(
        f"⛏️ **سیستم ماینر**\n\n"
        f"💰 **تولید**: {miner_income} ZP/ساعت\n"
        f"📊 **سطح**: {user[9]}\n"
        f"💎 **موجودی**: {user[10]} ZP\n"
        f"🔼 **هزینه ارتقا**: {user[9] * 500} ZP\n\n"
        f"⏰ هر ساعت می‌توانید برداشت کنید\n"
        f"برای برداشت: <code>برداشت ماینر</code>",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "📦 جعبه")
async def boxes_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📦 جعبه برنزی"), types.KeyboardButton(text="🥈 جعبه نقره‌ای")],
            [types.KeyboardButton(text="🔙 منوی اصلی")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "📦 **جعبه‌های شانس**\n\n"
        "📦 **برنزی** - رایگان (هر ۲۴ ساعت)\n"
        "• ۵۰-۲۰۰ ZP\n"
        "• موشک معمولی\n\n"
        "🥈 **نقره‌ای** - ۲,۰۰۰ ZP\n"
        "• ۲۰۰-۵۰۰ ZP\n"
        "• موشک ویژه\n\n"
        "👇 جعبه مورد نظر را انتخاب کنید:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "📦 جعبه برنزی")
async def bronze_box_handler(message: types.Message):
    user = get_user(message.from_user.id)
    
    # شانس‌ها
    reward_type = random.choices(
        ['zp', 'missile'],
        weights=[70, 30]
    )[0]
    
    if reward_type == 'zp':
        reward = random.randint(50, 200)
        update_user_zp(message.from_user.id, reward)
        response = f"📦 **جعبه برنزی** 🎉\n\n💰 **جایزه**: {reward} ZP"
    else:
        missile = random.choice(list(MISSILE_PRICES.keys())[:2])  # فقط موشک‌های ارزان
        add_missile(message.from_user.id, missile, 1)
        response = f"📦 **جعبه برنزی** 🎉\n\n🚀 **جایزه**: ۱ عدد {missile}"
    
    response += f"\n\n💎 **موجودی جدید**: {get_user(message.from_user.id)[4]:,} ZP"
    await message.answer(response, reply_markup=main_menu())

@dp.message(lambda message: message.text in ["🛡 دفاع", "🕵️ خرابکاری", "🎯 ترکیب‌ها"])
async def coming_soon_handler(message: types.Message):
    feature_name = {
        "🛡 دفاع": "سیستم دفاع",
        "🕵️ خرابکاری": "سیستم خرابکاری", 
        "🎯 ترکیب‌ها": "سیستم ترکیب‌ها"
    }[message.text]
    
    await message.answer(
        f"🛠 **{feature_name}**\n\n"
        f"🔜 به زودی فعال می‌شود\n\n"
        f"در حال حاضر می‌توانید از:\n"
        f"• ⚔️ سیستم حمله\n"
        f"• 🛒 فروشگاه\n"
        f"• ⛏ ماینر\n"
        f"• 📦 جعبه‌ها\n"
        f"استفاده کنید!",
        reply_markup=main_menu()
    )

@dp.message(lambda message: message.text == "🔙 منوی اصلی")
async def back_handler(message: types.Message):
    await message.answer("🔙 بازگشت به منوی اصلی", reply_markup=main_menu())

# هندلر پیام‌های متنی
@dp.message()
async def all_messages(message: types.Message):
    text = message.text.lower()
    
    if "خرید" in text and "موشک" in text:
        # استخراج نام موشک
        missile_name = text.replace("خرید", "").replace("موشک", "").strip()
        
        if missile_name in MISSILE_PRICES:
            user = get_user(message.from_user.id)
            price = MISSILE_PRICES[missile_name]
            
            if user[4] >= price:
                update_user_zp(message.from_user.id, -price)
                add_missile(message.from_user.id, missile_name, 1)
                
                await message.answer(
                    f"✅ **خرید موفق**\n\n"
                    f"🚀 **موشک**: {missile_name}\n"
                    f"💰 **قیمت**: {price:,} ZP\n"
                    f"💎 **موجودی جدید**: {user[4] - price:,} ZP",
                    reply_markup=main_menu()
                )
            else:
                await message.answer(
                    f"❌ **موجودی ناکافی**\n\n"
                    f"💰 **قیمت**: {price:,} ZP\n"
                    f"💎 **موجودی شما**: {user[4]:,} ZP\n"
                    f"📉 **کمبود**: {price - user[4]:,} ZP",
                    reply_markup=main_menu()
                )
        else:
            await message.answer("❌ موشک پیدا نشد! نام موشک را درست وارد کنید.")
    
    elif "برداشت" in text and "ماینر" in text:
        user = get_user(message.from_user.id)
        if user[10] > 0:
            update_user_zp(message.from_user.id, user[10])
            db.conn.cursor().execute('UPDATE users SET miner_balance = 0 WHERE user_id = ?', (message.from_user.id,))
            db.conn.commit()
            
            await message.answer(
                f"⛏️ **برداشت موفق**\n\n"
                f"💰 **مبلغ**: {user[10]:,} ZP\n"
                f"💎 **موجودی جدید**: {get_user(message.from_user.id)[4]:,} ZP",
                reply_markup=main_menu()
            )
        else:
            await message.answer("❌ موجودی ماینر شما صفر است!", reply_markup=main_menu())
    
    else:
        await message.answer("🎯 از منوی زیر انتخاب کنید:", reply_markup=main_menu())

# شروع بات
async def main():
    print("🔄 اتصال به تلگرام...")
    
    # حذف وب‌هوک
    async with aiohttp.ClientSession() as session:
        await session.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
        print("✅ وب‌هوک حذف شد")
    
    # اطلاعات بات
    bot_info = await bot.get_me()
    print(f"✅ بات: @{bot_info.username}")
    
    print("🚀 شروع دریافت پیام‌ها...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
