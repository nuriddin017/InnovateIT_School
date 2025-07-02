# handlers.py

from telegram import Update
from telegram.ext import CallbackContext
from config import ADMIN_IDS,  ADMIN_USERNAMES, payments
from datetime import datetime
from utils import is_admin, format_payment_status

import json
import csv


# Start komandasi
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! To‘lov holatini tekshirish uchun /status deb yozing.")

# Status komandasi
def status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if str(user_id) in payments:
        if payments[str(user_id)]:
            update.message.reply_text("✅ Sizning to‘lovingiz QILINDI.")
        else:
            update.message.reply_text("❌ Sizning to‘lovingiz HALI QILINMAGAN.")
    else:
        admins = "\n".join(ADMIN_USERNAMES)
        update.message.reply_text(
            f"🚫 Siz ro‘yxatda mavjud emassiz.\n"
            f"Iltimos, admin bilan bog‘laning:\n{admins}"
        )

# Admin tekshiruvchi funksiya
def is_admin(user_id):
    return user_id in ADMIN_IDS

# Pay komandasi (faqat adminlar uchun)
def pay(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("⛔ Sizga bu komandani ishlatishga ruxsat yo‘q.")
        return

    try:
        target_id = context.args[0]
        if target_id in payments:
            payments[target_id] = True
            save_payments()
            update.message.reply_text(f"✅ {target_id} to‘lov qilgan deb belgilandi.")
        else:
            update.message.reply_text("❗ Bu foydalanuvchi ro‘yxatda yo‘q.")
    except:
        update.message.reply_text("❗ To‘g‘ri format: /pay <foydalanuvchi_id>")

# Unpay komandasi (faqat adminlar uchun)
def unpay(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("⛔ Sizga bu komandani ishlatishga ruxsat yo‘q.")
        return

    try:
        target_id = context.args[0]
        if target_id in payments:
            payments[target_id] = False
            save_payments()
            update.message.reply_text(f"❌ {target_id} to‘lov qilmagan deb belgilandi.")
        else:
            update.message.reply_text("❗ Bu foydalanuvchi ro‘yxatda yo‘q.")
    except:
        update.message.reply_text("❗ To‘g‘ri format: /unpay <foydalanuvchi_id>")

# JSON faylga yozib borish (data saqlansin)
def save_payments():
    with open("data/payments.json", "w") as f:
        json.dump(payments, f, indent=4)


# handlers.py (davomi)

# Foydalanuvchi qo‘shish komandasi (faqat adminlar uchun)
def add(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("⛔ Sizga bu komandani ishlatishga ruxsat yo‘q.")
        return

    try:
        target_id = context.args[0]
        if target_id in payments:
            update.message.reply_text("⚠️ Bu foydalanuvchi allaqachon ro‘yxatda mavjud.")
        else:
            payments[target_id] = False  # boshlanishda hali to‘lamagan
            save_payments()
            update.message.reply_text(f"✅ {target_id} ro‘yxatga qo‘shildi. To‘lov holati: HALI QILINMAGAN.")
    except:
        update.message.reply_text("❗ Format noto‘g‘ri. To‘g‘ri format: /add <foydalanuvchi_id>")

        
def list_unpaid(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("⛔ Sizga bu komandani ishlatishga ruxsat yo‘q.")
        return

    unpaid_users = [uid for uid, paid in payments.items() if not paid]

    if not unpaid_users:
        update.message.reply_text("🎉 Hamma foydalanuvchilar to‘lov qilgan!")
    else:
        msg = "❌ To‘lov qilmagan foydalanuvchilar ID ro‘yxati:\n"
        msg += "\n".join(unpaid_users)
        update.message.reply_text(msg)


def export_csv(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        update.message.reply_text("⛔ Sizga bu komandani ishlatishga ruxsat yo‘q.")
        return

    with open("data/payments.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User ID", "To‘lov holati"])
        for uid, paid in payments.items():
            writer.writerow([uid, "Qilgan" if paid else "Qilmagan"])

    update.message.reply_text("📥 payments.csv faylga eksport qilindi.")



    
# utils.py



# ✅ Admin tekshirish
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ✅ User ID to‘g‘riligini tekshirish (masalan: /pay 123456789)
def is_valid_user_id(text: str) -> bool:
    return text.isdigit() and len(text) >= 6

# ✅ To‘lov statusini emoji bilan ko‘rsatish
def format_payment_status(paid: bool) -> str:
    return "✅ Qilgan" if paid else "❌ Qilmagan"

# ✅ Sana va vaqtni formatlash (bugungi sana: 2025-07-02 14:10)
def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# ✅ CSV yoki PDF fayl nomi uchun dinamik nom yaratish
def generate_filename(base: str = "payments", ext: str = "csv") -> str:
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"{base}_{date_str}.{ext}"

# ✅ To‘lov statistikasi: jami, qilgan, qilmagan
def get_payment_stats() -> dict:
    total = len(payments)
    paid = sum(1 for v in payments.values() if v)
    unpaid = total - paid
    return {
        "jami": total,
        "qilgan": paid,
        "qilmagan": unpaid
    }

