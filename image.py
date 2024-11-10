from vk_api.upload import VkUpload
from vk_api import VkApi
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Настройка
TOKEN = 'vk1.a.KwYHDEIMWw6VMI5lTIcNrgVH9886g_A-7dIO6LTWXAor7Ezz61anAD1U3Z397O55phaBtK2vjcLiVKUCaQYJwhxIKkAVYWE_y7X_YXrLoani2VkeglEfHMkXerMYGq_RtrIGmjX-2_FhGbzCbKBmzKPTDPTdo2HmvzdiwrFPHCVWiFhsZk61QEVgHqlVcUC9Ss-piU3iJBngplw8UsITvw'
album_id = '303285069'

# Инициализация VK API
vk_session = VkApi(token=TOKEN)
vk = vk_session.get_api()

def upload_photo(photo_path):
    try:
        # Загрузка фото
        photo = VkUpload(vk)
        uploaded_photo = photo.photo(photo_path, album_id)
        
        return f'Фото успешно загружено. ID: {uploaded_photo[0]}'
    except Exception as e:
        logging.error(f"Ошибка при загрузке фото: {str(e)}")
        return f"Произошла ошибка при загрузке фото: {str(e)}"

def main():
    # Проверяем наличие файла
    file_path = 'C:/Dev/conditery_vkbot/moskva.jpeg'
    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        return
    
    # Загружаем фото
    result = upload_photo(file_path)
    logging.info(result)

if __name__ == "__main__":
    main()
