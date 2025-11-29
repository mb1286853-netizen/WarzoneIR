import requests
import time
import os

TOKEN = os.getenv("TOKEN")

print(f"🔑 توکن: {TOKEN}")

def get_updates():
    """دریافت پیام‌ها"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

def send_message(chat_id, text):
    """ارسال پیام"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=data)
    return response.json()

# تست اولیه
print("🧪 تست توکن...")
test = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe").json()
print(f"نتیجه تست: {test}")

if test.get("ok"):
    print("✅ بات فعال است! در حال گوش دادن...")
    last_update_id = 0
    
    while True:
        updates = get_updates()
        if updates.get("ok"):
            for update in updates["result"]:
                if update["update_id"] > last_update_id:
                    last_update_id = update["update_id"]
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"]["text"]
                    
                    print(f"📩 پیام: {text}")
                    send_message(chat_id, "🤖 بات فعال است!")
        
        time.sleep(1)
else:
    print("❌ توکن نامعتبر است!")
