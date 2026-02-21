from datetime import datetime
from m8.fjurur.database import get_schedule

DAYS_TRANSLATION = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}

def get_today_schedule(class_number):
    today_eng = datetime.now().strftime("%A")
    today_ru = DAYS_TRANSLATION.get(today_eng, today_eng)

    lessons = get_schedule(class_number, today_ru)

    if not lessons:
        return f"Сегодня ({today_ru}) занятий нет 🎉"

    text = f"📚 Расписание на {today_ru}:\n\n"
    text += "\n".join(lessons)

    return text


def get_full_schedule(class_number):
    schedule_days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

    text = f"📚 Полное расписание {class_number} класса:\n"

    for day in schedule_days:
        lessons = get_schedule(class_number, day)

        if lessons:
            text += f"\n📅 {day}\n"
            text += "\n".join(lessons) + "\n"

    return text