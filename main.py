from telegram.ext import ApplicationBuilder, CommandHandler
import os
from handlers import start, status, pay, unpay, add, list_unpaid, export_csv
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("unpay", unpay))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_unpaid))
    app.add_handler(CommandHandler("export", export_csv))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()