import os
import sqlite3


def create_database():
    try:
        conn = sqlite3.connect('conditery_db.sqlite')
        cursor = conn.cursor()

        # Создаем таблицу products с колонкой для ссылок на изображения
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            description TEXT,
            image_url TEXT
        )''')

        print("База данных и таблица успешно созданы.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        if (conn):
            conn.close()
            print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    create_database()