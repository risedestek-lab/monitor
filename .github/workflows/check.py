import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT_TOKEN:", BOT_TOKEN)
print("CHAT_ID:", CHAT_ID)

URL = "https://www.risebet249.com/"

try:
    r = requests.get(URL, timeout=10)
    print("STATUS:", r.status_code)

    if r.status_code == 200:
        text = "✅ Site aktif kral"
    else:
        text = f"⚠️ Site sorunlu: {r.status_code}"
except Exception as e:
    print("ERROR:", e)
    text = "🚨 Site çöktü kral!"

res = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": text}
)

print("TELEGRAM RESPONSE:", res.text)
