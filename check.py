import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DOMAINS = [
    "https://www.risebet248.com/",
    "https://www.risebet249.com/",
    "https://www.risebet250.com/",
    "https://www.risebet251.com/",
    "https://www.risebet252.com/",
    "https://www.risebet253.com/",
    "https://www.risebet254.com/",
    "https://www.risebet255.com/",
    "https://www.risebet256.com/",
    "https://www.risebet257.com/",
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

import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DOMAINS = [
    "https://www.risebet249.com/"
]

PROXIES = [
    "http://185.199.229.156:7492",
    "http://51.158.68.68:8811",
    "http://103.152.112.162:80",
]

STATE_FILE = "status.json"

def check_with_proxy(url):
    for proxy in PROXIES:
        try:
            r = requests.get(
                url,
                proxies={"http": proxy, "https": proxy},
                timeout=8
            )
            return r.status_code
        except:
            continue
    return "TR_DOWN"

# eski durum
try:
    with open(STATE_FILE, "r") as f:
        old = json.load(f)
except:
    old = {}

new = {}

for site in DOMAINS:

    # global kontrol
    try:
        r = requests.get(site, timeout=8)
        global_status = r.status_code
    except:
        global_status = "DOWN"

    # TR kontrol (proxy)
    tr_status = check_with_proxy(site)

    new[site] = {"global": global_status, "tr": tr_status}

    if old.get(site) != new[site]:
        msg = f"""🚨 DURUM DEĞİŞTİ

🌍 Global: {global_status}
🇹🇷 TR: {tr_status}

🔗 {site}
"""
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg}
        )

# kaydet
with open(STATE_FILE, "w") as f:
    json.dump(new, f)
