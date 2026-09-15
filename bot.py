import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🛒 Добро пожаловать в ASC MARKET!\n\n"
        "Здесь можно размещать и находить объявления.\n\n"
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

bot.infinity_polling()
