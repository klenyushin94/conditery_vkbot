import json
import os
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api.keyboard import VkKeyboard
from vk_api import VkUpload
import sqlite3

# Токен вашего бота
TOKEN = 'vk1.a.KwYHDEIMWw6VMI5lTIcNrgVH9886g_A-7dIO6LTWXAor7Ezz61anAD1U3Z397O55phaBtK2vjcLiVKUCaQYJwhxIKkAVYWE_y7X_YXrLoani2VkeglEfHMkXerMYGq_RtrIGmjX-2_FhGbzCbKBmzKPTDPTdo2HmvzdiwrFPHCVWiFhsZk61QEVgHqlVcUC9Ss-piU3iJBngplw8UsITvw'

# Путь к изображению
image_path = "C:/Dev/conditery_vkbot/moskva.jpeg"

# ID сообщества (замените на реальный ID вашего сообщества)
community_id = 139829694  # Замените на реальный ID вашего сообщества

def send_photo(photo1):
    global attachment
    upload = VkUpload(vk_session)
    photo = upload.photo_messages(photo1)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'

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

def get_products_by_type(type_name):
    """
    Функция для получения списка продуктов определенного типа из базы данных.
    """
    conn, cursor = connect_to_database()
    
    query = """SELECT id, name, description FROM products WHERE type = ?"""
    cursor.execute(query, (type_name,))
    products = cursor.fetchall()
    
    conn.close()
    return products

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
            [{"action": {"type": "text", "label": "Торты"}}]
        ]
    }
    return json.dumps(keyboard)

def send_message(peer_id, message, attachments=None, keyboard=None):
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
            elif event.text.lower() == "картинка":
                send_photo('moskva.png')
                vk.messages.send(
                    peer_id = event.peer_id,
                    random_id = random.randint(100000, 200000),
                    attachment = attachment
                )
            elif event.text.lower() == "выпечка":
                products = get_products_by_type("Выпечка")
                if products:
                    message = "Есть следующая выпечка:\n\n"
                    for i, product in enumerate(products, start=1):
                        name, description = product[1], product[2]
                        message += f"{name}\nОписание: {description}\n\n"
                    send_message(event.peer_id, message, keyboard=create_greeting_2_buttons())
                else:
                    send_message(event.peer_id, "К сожалению, выпечки не найдено в базе данных.")
            elif event.text.lower() == "торты":
                torts = get_products_by_type("Торты")
                if torts:
                    message = "Есть следующие торты:\n\n"
                    for i, tort in enumerate(torts, start=1):
                        name, description = tort[1], tort[2]
                        message += f"{name}\nОписание: {description}\n\n"
                    send_message(event.peer_id, message, keyboard=create_greeting_2_buttons())
                else:
                    send_message(event.peer_id, "К сожалению, тортов не найдено в базе данных.")

