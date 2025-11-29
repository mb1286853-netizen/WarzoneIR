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

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ایمپورت هندلرها
from handlers import (
    start, profile, attack, combo_attacks, shop, 
    boxes, miner, defense, sabotage, support, admin
)

async def on_startup(app):
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    await bot.set_webhook(url=webhook_url)
    print(f"Webhook تنظیم شد: {webhook_url}")
    print("WarZone Bot ۲۴ ساعته و بدون خواب آنلاین شد! ⚔️")

def main():
    dp.startup.register(on_startup)
    
    # همه هندلرها
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

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    
    # صفحه اصلی برای تست
    async def index(request):
        return web.Response(text="WarZone Bot زنده‌ست! ⚔️")
    app.router.add_get("/", index)
    
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
