# main.py

from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import os
from handlers import (
    start, status, pay, unpay,
    add, list_unpaid, export_csv
)

# .env fayldan tokenni yuklaymiz
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def error_handler(update, context):
    print(f"⚠️ Xatolik: {context.error}")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Komandalarni ro‘yxatga olish
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("pay", pay))
    dp.add_handler(CommandHandler("unpay", unpay))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_unpaid))
    dp.add_handler(CommandHandler("export", export_csv))

    # Xatoliklar uchun handler
    dp.add_error_handler(error_handler)

    # Botni ishga tushuramiz
    print("🤖 Bot ishga tushdi...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
