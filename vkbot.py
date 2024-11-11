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
    return attachment

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

def get_products_by_name(name):
    """
    Функция для получения списка продуктов определенного типа из базы данных.
    """
    conn, cursor = connect_to_database()
    
    query = """SELECT id, name, type, description, image FROM products WHERE name = ?"""
    cursor.execute(query, (name,))
    products = cursor.fetchall()
    
    conn.close()
    return products


def create_greeting_buttons():
    """
    Создание клавиатуры с кнопками для выбора продукта.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Выпечка"}}],
            [{"action": {"type": "text", "label": "Торты"}}],
            [{"action": {"type": "text", "label": "Трайфлы"}}],
            [{"action": {"type": "text", "label": "Бенто-торты"}}]
        ]
    }
    return json.dumps(keyboard)


def create_greeting_buttons_2():
    """
    Создание клавиатуры с кнопками для выбора продукта.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Вернуться в главное меню"}}],
        ]
    }
    return json.dumps(keyboard)


def create_greeting_buttons_product():
    """
    Создание клавиатуры с кнопками для выбора торта.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Киевский"}}],
            [{"action": {"type": "text", "label": "Графские развалины"}}],
            [{"action": {"type": "text", "label": "Наполеон"}}],
            [{"action": {"type": "text", "label": "Вернуться в главное меню"}}],
        ]
    }
    return json.dumps(keyboard)

def create_greeting_buttons_baker():
    """
    Создание клавиатуры с кнопками для выбора выпечки.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Булка Московская"}}],
            [{"action": {"type": "text", "label": "Корзиночка с вишней"}}],
            [{"action": {"type": "text", "label": "Булка с маком"}}],
            [{"action": {"type": "text", "label": "Вернуться в главное меню"}}],
        ]
    }
    return json.dumps(keyboard)


def create_greeting_buttons_trifle():
    """
    Создание клавиатуры с кнопками для выбора трайфла.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Красный бархат"}}],
            [{"action": {"type": "text", "label": "Банановый трайфл"}}],
            [{"action": {"type": "text", "label": "Ягодный трайфл"}}],
            [{"action": {"type": "text", "label": "Вернуться в главное меню"}}],
        ]
    }
    return json.dumps(keyboard)


def create_greeting_buttons_bento():
    """
    Создание клавиатуры с кнопками для выбора трайфла.
    """
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [{"action": {"type": "text", "label": "Бетно-торт шоколадный"}}],
            [{"action": {"type": "text", "label": "Бенто-торт с черникой"}}],
            [{"action": {"type": "text", "label": "Бенто-торт с клубникой"}}],
            [{"action": {"type": "text", "label": "Вернуться в главное меню"}}],
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


def show_one_product(text):
    products = get_products_by_name(text)
    if products:
        for i, product in enumerate(products, start=1):
            message = ''
            name, type, description, image = product[1], product[2], product[3], product[4]
            message += f"{name}\nОписание: {description}\n\n"
            attachment = send_photo(image)
            send_message(event.peer_id, message)
            vk.messages.send(
                peer_id = event.peer_id,
                random_id = random.randint(100000, 200000),
                attachment = attachment,
                keyboard = create_greeting_buttons_2()
            )
    else:
        send_message(event.peer_id, "К сожалению, информации в базе данных нет", keyboard=create_greeting_buttons_2())


if __name__ == '__main__':
    print('Бот запущен!')
    for event in longpoll.listen():
        print(event.text.lower())
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            if event.text.lower() == "начать" or event.text.lower() == "вернуться в главное меню":
                send_message(event.peer_id, "Привет! Мы - кондитерская bylok.net! Выбери интересующую категорию", keyboard=create_greeting_buttons())
            elif event.text.lower() == "торты":
                send_message(event.peer_id, "Выберите торт", keyboard=create_greeting_buttons_product())
            elif event.text.lower() == "выпечка":
                send_message(event.peer_id, "Выберите выпечку", keyboard=create_greeting_buttons_baker())
            elif event.text.lower() == "трайфлы":
                send_message(event.peer_id, "Выберите трайфл", keyboard=create_greeting_buttons_trifle())
            elif event.text.lower() == "бенто-торты":
                send_message(event.peer_id, "Выберите бенто-торт", keyboard=create_greeting_buttons_bento())
            elif event.text.lower() == "киевский":
                show_one_product(event.text)
            elif event.text.lower() == "наполеон":
                show_one_product(event.text)
            elif event.text.lower() == "графские развалины":
                show_one_product(event.text)
            elif event.text.lower() == "корзиночка с вишней":
                show_one_product(event.text)
            elif event.text.lower() == "булка с маком":
                show_one_product(event.text)
            elif event.text.lower() == "булка московская":
                show_one_product(event.text)
            elif event.text.lower() == "красный бархат":
                show_one_product(event.text)
            elif event.text.lower() == "банановый трайфл":
                show_one_product(event.text)
            elif event.text.lower() == "ягодный трайфл":
                show_one_product(event.text)
            elif event.text.lower() == "бенто-торт шоколадный":
                show_one_product(event.text)
            elif event.text.lower() == "бенто-торт с черникой":
                show_one_product(event.text)
            elif event.text.lower() == "бенто-торт с клубникой":
                show_one_product(event.text)
            
            else:
                send_message(event.peer_id, "Я не понимаю ваш запрос. Выберите категорию десерта!", keyboard=create_greeting_buttons())
                