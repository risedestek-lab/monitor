import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DOMAINS = [
    "https://www.risebet249.com/",
    # buraya istediğin kadar domain ekle
]

STATE_FILE = "status.json"

# eski durumları yükle
try:
    with open(STATE_FILE, "r") as f:
        old_status = json.load(f)
except:
    old_status = {}

new_status = {}

for site in DOMAINS:
    try:
        r = requests.get(site, timeout=10)
        status = r.status_code
    except:
        status = "DOWN"

    new_status[site] = status

    # değişiklik varsa mesaj at
    if old_status.get(site) != status:
        msg = f"🚨 {site} durumu değişti: {status}"
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg}
        )

# yeni durumu kaydet
with open(STATE_FILE, "w") as f:
    json.dump(new_status, f)
