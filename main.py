import telebot
from database import init_db
from logic import register_handlers

TOKEN = "YOUR_TOKEN"  # <-- вставь токен

bot = telebot.TeleBot(TOKEN)

init_db()
register_handlers(bot)

print("Бот запущен...")
bot.polling()
