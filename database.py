import sqlite3

DB_NAME = "school.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class INTEGER,
            day TEXT,
            lesson TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_lesson(class_number, day, lesson):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO schedule (class, day, lesson) VALUES (?, ?, ?)",
        (class_number, day, lesson)
    )

    conn.commit()
    conn.close()


def delete_lesson(class_number, day, lesson):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM schedule WHERE class=? AND day=? AND lesson=?",
        (class_number, day, lesson)
    )

    conn.commit()
    conn.close()


def get_schedule(class_number, day):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT lesson FROM schedule WHERE class=? AND day=?",
        (class_number, day)
    )

    lessons = cursor.fetchall()
    conn.close()

    return [lesson[0] for lesson in lessons]
