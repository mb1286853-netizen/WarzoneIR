print("🚀 WarZone Bot Starting...")

try:
    from aiohttp import web
    print("✅ aiohttp imported successfully")
    
    async def health_check(request):
        return web.Response(text="✅ WarZone Bot - Health Check OK")
    
    app = web.Application()
    app.router.add_get('/', health_check)
    
    print("✅ Web server configured")
    web.run_app(app, host='0.0.0.0', port=8000)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
