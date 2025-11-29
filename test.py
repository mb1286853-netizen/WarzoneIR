print("✅ Python is working!")
try:
    import aiogram
    print("✅ Aiogram imported successfully!")
except ImportError as e:
    print(f"❌ Aiogram import failed: {e}")

try:
    from database import Database
    db = Database()
    print("✅ Database initialized!")
except Exception as e:
    print(f"❌ Database error: {e}")
