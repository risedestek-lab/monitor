import requests
import os
from concurrent.futures import ThreadPoolExecutor

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DOMAINS = [
    "https://www.risebet248.com/",
    "https://www.risebet249.com/",
    "https://www.risebet250.com/",
]

PROXIES = [
    "http://185.199.229.156:7492",
    "http://51.158.68.68:8811",
    "http://103.152.112.162:80",
]

def check_site(site):
    try:
        r = requests.get(site, timeout=6)
        global_status = r.status_code
    except:
        global_status = "DOWN"

    tr_status = "TR_DOWN"
    for proxy in PROXIES:
        try:
            r = requests.get(site, proxies={"http": proxy, "https": proxy}, timeout=6)
            tr_status = r.status_code
            break
        except:
            continue

    return site, global_status, tr_status


results = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_site, site) for site in DOMAINS]
    for f in futures:
        results.append(f.result())


msg = "📊 DOMAIN RAPORU\n\n"

for site, g, tr in results:
    durum = "✅"

    if g != 200:
        durum = "❌ GLOBAL DOWN"
    elif g == 200 and tr != 200:
        durum = "🚨 TR ENGEL"

    msg += f"{durum}\n🌍 {g} | 🇹🇷 {tr}\n🔗 {site}\n\n"


requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": msg}
)
