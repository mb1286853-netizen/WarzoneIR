import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن بات پیدا نشد! .env رو چک کن")

# تنظیمات لاگ برای مانیتورینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ایمپورت هندلرها
from handlers import (
    start, profile, attack, combo_attacks, shop, 
    boxes, miner, defense, sabotage, support, admin
)

async def on_startup(app):
    """فعال شدن بات"""
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    await bot.set_webhook(url=webhook_url)
    logging.info(f"Webhook تنظیم شد: {webhook_url}")
    logging.info("WarZone Bot ۲۴ ساعته و بدون خواب آنلاین شد! ⚔️")

async def on_shutdown(app):
    """خاموش شدن بات"""
    logging.info("بات در حال خاموش شدن...")
    await bot.session.close()

def main():
    # ثبت هندلر استارتاپ و شات‌داون
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # ثبت تمام روترها
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(attack.router)
    dp.include_router(combo_attacks.router)
    dp.include_router(shop.router)
    dp.include_router(boxes.router)
    dp.include_router(miner.router)
    dp.include_router(defense.router)
    dp.include_router(sabotage.router)
    dp.include_router(support.router)
    dp.include_router(admin.router)

    # ساخت اپلیکیشن aiohttp
    app = web.Application()
    
    # ثبت وب‌هوک
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    
    # صفحه اصلی برای چک کردن سلامت بات
    async def health_check(request):
        return web.Response(
            text="🟢 WarZone Bot زنده و فعال است! ⚔️\n\n"
                 "✅ بات بدون استراحت در حال کار است\n"
                 "✅ تمام سیستم‌ها فعال\n"
                 "✅ دیتابیس متصل\n"
                 f"🚀 آخرین آپتایم: {web.datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    
    # گرفتن پورت از محیط رندر
    port = int(os.environ.get("PORT", 8000))
    
    # اجرای اپلیکیشن - بدون هیچ استراحتی
    web.run_app(
        app, 
        host="0.0.0.0", 
        port=port,
        # هیچ timeout یا استراحتی وجود ندارد
        access_log=None  # برای کاهش لاگ‌ها
    )

if __name__ == "__main__":
    # اجرای مستقیم بات
    main()
