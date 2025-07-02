# config.py

import os
import json
from dotenv import load_dotenv

# ✅ .env faylni yuklaymiz
load_dotenv()

# ✅ Telegram bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Admin ID larni int tipida olish (agar mavjud bo‘lsa)
ADMIN_IDS = []
admin_ids_raw = os.getenv("ADMIN_IDS", "")
if admin_ids_raw:
    ADMIN_IDS = list(map(int, admin_ids_raw.split(",")))

# ✅ Admin username lar ro‘yxati (e.g. @admin1, @admin2)
ADMIN_USERNAMES = os.getenv("ADMIN_USERNAMES", "").split(",")

# ✅ Foydalanuvchilar va to‘lov holatlari
PAYMENTS_FILE = "data/payments.json"
try:
    with open(PAYMENTS_FILE, "r") as f:
        payments = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    payments = {}
