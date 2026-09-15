import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ads = {}

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


@bot.message_handler(commands=["add"])
def add_start(message):
    ads[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "📂 Напиши категорию объявления.\n\n"
        "Например: Авто, Запчасти, Услуги, Товары."
    )


@bot.message_handler(
    func=lambda message:
    message.chat.id in ads and "category" not in ads[message.chat.id]
)
def get_category(message):
    ads[message.chat.id]["category"] = message.text
    bot.send_message(
        message.chat.id,
        "✏️ Напиши название объявления."
    )


@bot.message_handler(
    func=lambda message:
    message.chat.id in ads and "title" not in ads[message.chat.id]
)
def get_title(message):
    ads[message.chat.id]["title"] = message.text
    bot.send_message(
        message.chat.id,
        "💰 Напиши цену."
    )


@bot.message_handler(
    func=lambda message:
    message.chat.id in ads and "price" not in ads[message.chat.id]
)
def get_price(message):
    ads[message.chat.id]["price"] = message.text
    bot.send_message(
        message.chat.id,
        "📝 Напиши описание."
    )


@bot.message_handler(
    func=lambda message:
    message.chat.id in ads and "description" not in ads[message.chat.id]
)
def get_description(message):
    ads[message.chat.id]["description"] = message.text
    bot.send_message(
        message.chat.id,
        "📸 Теперь отправь фотографию объявления."
    )


@bot.message_handler(
    content_types=["photo"],
    func=lambda message:
    message.chat.id in ads and
    "description" in ads[message.chat.id] and
    "photo" not in ads[message.chat.id]
)
def get_photo(message):
    ads[message.chat.id]["photo"] = message.photo[-1].file_id

    ad = ads[message.chat.id]

    text = (
        "📋 ПРЕДПРОСМОТР ОБЪЯВЛЕНИЯ\n\n"
        f"📂 Категория: {ad['category']}\n"
        f"📌 {ad['title']}\n"
        f"💰 Цена: {ad['price']}\n"
        f"📝 {ad['description']}\n\n"
        "📸 Фото добавлено.\n\n"
        "⚠️ Пока это тестовая публикация."
    )

    bot.send_photo(
        message.chat.id,
        ad["photo"],
        caption=text
    )

    del ads[message.chat.id]


threading.Thread(target=run_server, daemon=True).start()

bot.infinity_polling()
