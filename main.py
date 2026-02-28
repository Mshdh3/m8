import telebot
from config import BOT_TOKEN
from database import init_db
from logic import register_handlers

bot = telebot.TeleBot(TOKEN)

init_db()
register_handlers(bot)

print("Бот запущен...")
bot.polling()

