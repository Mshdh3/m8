from database import get_schedule, add_lesson, delete_lesson

user_class = {}

ADMIN_ID = 123456789  # <-- ВСТАВЬ СВОЙ TELEGRAM ID

DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
]


def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            message.chat.id,
            "👋 Привет!\n"
            "Напиши номер своего класса (1–11)"
        )

    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot.send_message(
            message.chat.id,
            "📚 Команды бота:\n\n"
            "/start — начать\n"
            "/help — помощь\n\n"
            "👩‍🎓 Ученик:\n"
            "1. Напиши номер класса\n"
            "2. Напиши день недели (например: Среда)\n\n"
            "👨‍🏫 Админ:\n"
            "/add класс день урок\n"
            "/delete класс день урок"
        )

    @bot.message_handler(commands=['add'])
    def add(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "⛔ Нет доступа")
            return

        try:
            parts = message.text.split(maxsplit=3)
            class_number = int(parts[1])
            day = parts[2].capitalize()
            lesson = parts[3]

            if day not in DAYS:
                bot.send_message(message.chat.id, "❌ Неверный день недели")
                return

            add_lesson(class_number, day, lesson)
            bot.send_message(message.chat.id, "✅ Урок добавлен")

        except:
            bot.send_message(
                message.chat.id,
                "Формат: /add класс день урок\n"
                "Пример: /add 5 Понедельник Математика"
            )

    @bot.message_handler(commands=['delete'])
    def delete(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "⛔ Нет доступа")
            return

        try:
            parts = message.text.split(maxsplit=3)
            class_number = int(parts[1])
            day = parts[2].capitalize()
            lesson = parts[3]

            delete_lesson(class_number, day, lesson)
            bot.send_message(message.chat.id, "🗑 Урок удалён")

        except:
            bot.send_message(
                message.chat.id,
                "Формат: /delete класс день урок"
            )

    @bot.message_handler(func=lambda m: m.text.isdigit())
    def set_class(message):
        class_number = int(message.text)

        if class_number < 1 or class_number > 11:
            bot.send_message(message.chat.id, "Класс должен быть от 1 до 11")
            return

        user_class[message.chat.id] = class_number

        bot.send_message(
            message.chat.id,
            "Теперь напиши день недели\n"
            "(например: Среда)"
        )

    @bot.message_handler(func=lambda m: True)
    def show_schedule(message):
        class_number = user_class.get(message.chat.id)

        if not class_number:
            bot.send_message(message.chat.id, "Сначала напиши номер класса")
            return

        day = message.text.strip().capitalize()

        if day not in DAYS:
            bot.send_message(message.chat.id, "Введите корректный день недели")
            return

        lessons = get_schedule(class_number, day)

        if not lessons:
            bot.send_message(
                message.chat.id,
                f"📅 На {day} занятий нет 🎉"
            )
        else:
            text = f"📚 Расписание {class_number} класса на {day}:\n\n"
            text += "\n".join(lessons)
            bot.send_message(message.chat.id, text)
