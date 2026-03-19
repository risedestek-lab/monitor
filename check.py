import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URLS = [
    "https://www.risebet249.com/",
]

STATE_FILE = "state.json"

def send_msg(text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text}
    )

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

state = load_state()

for url in URLS:
    try:
        r = requests.get(url, timeout=10)
        is_up = r.status_code == 200
    except:
        is_up = False

    last_status = state.get(url)

    if last_status is None:
        state[url] = is_up
        continue

    if last_status and not is_up:
        send_msg(f"🚨 DOWN: {url}")
    elif not last_status and is_up:
        send_msg(f"✅ UP: {url}")

    state[url] = is_up

save_state(state)
