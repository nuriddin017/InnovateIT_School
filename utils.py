from config import ADMIN_IDS, payments, PAYMENTS_FILE
from datetime import datetime

# ✅ Admin ekanligini tekshiruvchi funksiya
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ✅ Foydalanuvchi ID'si integer formatda ekanligini tekshirish
def is_valid_user_id(text: str) -> bool:
    return text.isdigit() and len(text) >= 6  # Telegram ID kamida 6 raqamdan iborat

# ✅ User ID ni matn sifatida formatlash
def format_user_id(user_id: int) -> str:
    return f"`{user_id}`"

# ✅ To‘lov holatini chiroyli matnga aylantirish
def format_payment_status(paid: bool) -> str:
    return "✅ Qilgan" if paid else "❌ Qilmagan"

# ✅ Hozirgi sana/vaqtni chiroyli formatda qaytarish
def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# ✅ CSV yoki boshqa fayllar uchun avtomatik fayl nomi yaratish
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

# ✅ payments.json faylini saqlovchi funksiya
def save_payments_to_file(filepath="data/payments.json"):
    import json
    with open(filepath, "w") as f:
        json.dump(payments, f, indent=4)
        
def save_payments_to_file(filepath=PAYMENTS_FILE):
    import json
    with open(filepath, "w") as f:
        json.dump(payments, f, indent=4)