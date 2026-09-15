import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ASC MARKET Bot is running!")

def run_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🛒 Добро пожаловать в ASC MARKET!\n\n"
        "📢 /add — разместить объявление\n"
        "📋 /myads — мои объявления\n"
        "❓ /help — помощь"
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📢 /add — разместить объявление\n"
        "📋 /myads — мои объявления"
    )

threading.Thread(target=run_server, daemon=True).start()
bot.infinity_polling()
