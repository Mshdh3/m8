import asyncio
from aiogram import Bot, Dispatcher
from m8.fjurur.config import BOT_TOKEN
from m8.fjurur.database import init_db
from m8.fjurur.logic import register_handlers

async def main():
    while True:
        try:
            print("Бот запущен...")

            bot = Bot(token=BOT_TOKEN)
            dp = Dispatcher()

            # Инициализация базы данных
            init_db()

            # Подключение обработчиков
            register_handlers(dp)

            await dp.start_polling(bot)

        except Exception as e:
            print("Ошибка бота:", e)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())