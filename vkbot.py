import json
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api.keyboard import VkKeyboard
import sqlite3

# Токен вашего бота
TOKEN = 'vk1.a.KwYHDEIMWw6VMI5lTIcNrgVH9886g_A-7dIO6LTWXAor7Ezz61anAD1U3Z397O55phaBtK2vjcLiVKUCaQYJwhxIKkAVYWE_y7X_YXrLoani2VkeglEfHMkXerMYGq_RtrIGmjX-2_FhGbzCbKBmzKPTDPTdo2HmvzdiwrFPHCVWiFhsZk61QEVgHqlVcUC9Ss-piU3iJBngplw8UsITvw'
  # Замените на реальный токен

# Подключение к API VK и создание объекта LongPoll
vk_session = VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def connect_to_database():
    """
    Функция для подключения к базе данных SQLite.
    """
    conn = sqlite3.connect('conditery_db.sqlite')
    cursor = conn.cursor()
    return conn, cursor

def get_tort_products():
    """
    Функция для получения списка всех тортов из базы данных.
    """
    conn, cursor = connect_to_database()
    
    query = """SELECT id, name, description FROM products WHERE type = ?"""
    cursor.execute(query, ("Торты",))
    torts = cursor.fetchall()
    
    conn.close()
    return torts

def create_greeting_buttons():
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Хочу купить вкусняшку"}}]
        ]
    }
    return json.dumps(keyboard)

def create_greeting_2_buttons():
    """
    Создание клавиатуры с кнопками для выбора продукта.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Выпечка"}}],
            [{"action": {"type": "text", "label": "Торт"}}]
        ]
    }
    return json.dumps(keyboard)

def send_message(peer_id, message, keyboard=None):
    """
    Функция для отправки сообщений пользователю.
    """
    vk.messages.send(
        peer_id=peer_id,
        message=message,
        random_id=random.randint(100000, 200000),
        keyboard=keyboard
    )

if __name__ == '__main__':
    print('Бот запущен!')
    
    # Основной цикл бота
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            if event.text.lower() == "начать":
                send_message(event.peer_id, "Привет! Мы - кондитерская Bylok.net! Чего же ты хочешь?", keyboard=create_greeting_buttons())
            elif event.text.lower() == "хочу купить вкусняшку":
                send_message(event.peer_id, "Что именно ты хочешь?", keyboard=create_greeting_2_buttons())
            elif event.text.lower() == "выпечка":
                send_message(event.peer_id, "Пирожных пока нет в наличии! Выбери что нибудь другое!", keyboard=create_greeting_2_buttons())
            elif event.text.lower() == "торт":
                torts = get_tort_products()
                if torts:
                    message = "Есть следующие торты:\n\n"
                    for i, tort in enumerate(torts, start=1):
                        name, description = tort[1], tort[2]
                        message += f"{name}Описание: {description}\n\n"
                    send_message(event.peer_id, message, keyboard=create_greeting_2_buttons())
                else:
                    send_message(event.peer_id, "К сожалению, торты не найдены в базе данных.")
