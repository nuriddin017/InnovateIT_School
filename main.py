from telegram.ext import ApplicationBuilder, CommandHandler
import os
from handlers import start, status, pay, unpay, add, list_unpaid, export_csv
from flask import Flask
import threading
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask app (Render uchun HTTP endpoint)
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 InnovateIT School Bot ishlamoqda!"

@app.route("/healthz")
def health_check():
    return "OK"

def run_bot():
    """Telegram botni alohida thread da ishga tushirish"""
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("status", status))
    telegram_app.add_handler(CommandHandler("pay", pay))
    telegram_app.add_handler(CommandHandler("unpay", unpay))
    telegram_app.add_handler(CommandHandler("add", add))
    telegram_app.add_handler(CommandHandler("list", list_unpaid))
    telegram_app.add_handler(CommandHandler("export", export_csv))
    
    print("🤖 Bot ishga tushdi...")
    telegram_app.run_polling()

if __name__ == "__main__":
    # Bot ni alohida thread da ishga tushirish
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # HTTP server ishga tushirish (Render uchun)
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 HTTP server {port} portda ishga tushdi...")
    app.run(host="0.0.0.0", port=port, debug=False)