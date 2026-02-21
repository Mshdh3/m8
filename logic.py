from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from m8.fjurur.schedule_service import get_today_schedule
from m8.fjurur.database import add_lesson, delete_lesson, get_schedule
from m8.fjurur.config import ADMIN_ID

user_class = {}

DAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

def class_menu():
    buttons = []

    for i in range(1, 12):
        buttons.append([KeyboardButton(text=f"{i} класс")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def register_handlers(dp):

    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer(
            "👋 Добро пожаловать!\nВыберите класс:",
            reply_markup=class_menu()
        )

    @dp.message(Command("help"))
    async def help_handler(message: types.Message):
        await message.answer("""
🤖 Команды:

/start — начать
/help — помощь

📌 Студент:
• Выберите класс
• Напишите день недели
• Напишите "расписание"

👨‍🏫 Админ:
/add класс день урок
/delete класс день урок
""")

    @dp.message(lambda m: "класс" in m.text)
    async def set_class(message: types.Message):
        try:
            class_number = int(message.text.split()[0])
            user_class[message.from_user.id] = class_number

            await message.answer(
                f"Вы выбрали {class_number} класс.\nНапишите день недели или 'расписание'."
            )
        except:
            await message.answer("Ошибка выбора класса.")

    @dp.message(lambda m: m.text and m.text.lower() == "расписание")
    async def today_schedule(message: types.Message):
        class_number = user_class.get(message.from_user.id)

        if not class_number:
            await message.answer("Сначала выберите класс.")
            return

        schedule = get_today_schedule(class_number)
        await message.answer(schedule)

    @dp.message(lambda m: m.text and m.text.strip().capitalize() in DAYS)
    async def day_schedule(message: types.Message):
        class_number = user_class.get(message.from_user.id)

        if not class_number:
            await message.answer("Сначала выберите класс.")
            return

        day = message.text.strip().capitalize()
        lessons = get_schedule(class_number, day)

        if not lessons:
            await message.answer(f"📅 На {day} занятий нет 🎉")
            return

        text = f"📚 Расписание {class_number} класса на {day}:\n\n"
        text += "\n".join(lessons)

        await message.answer(text)

    @dp.message(lambda m: m.from_user.id == ADMIN_ID and m.text.startswith("/add"))
    async def add_handler(message: types.Message):
        try:
            parts = message.text.split(maxsplit=3)

            class_number = int(parts[1])
            day = parts[2].capitalize()
            lesson = parts[3]

            add_lesson(class_number, day, lesson)

            await message.answer("✅ Урок добавлен")
        except:
            await message.answer("❌ Формат: /add класс день урок")

    @dp.message(lambda m: m.from_user.id == ADMIN_ID and m.text.startswith("/delete"))
    async def delete_handler(message: types.Message):
        try:
            parts = message.text.split(maxsplit=3)

            class_number = int(parts[1])
            day = parts[2].capitalize()
            lesson = parts[3]

            delete_lesson(class_number, day, lesson)

            await message.answer("❌ Урок удалён")
        except:
            await message.answer("❌ Формат: /delete класс день урок")