import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает 🚀")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
