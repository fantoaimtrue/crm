import time
import hashlib
import hmac
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import requests
from decouple import config, Csv

router = Router()

# Инициализация подключения к БД
try:
    from db import create_user
except ImportError:
    print("Не удалось импортировать модуль БД.")

BOT_TOKEN = config('BOT_TOKEN')
BASE_URL = 'https://crmmarketplacehelper.ru/'

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    user_data = {
        'id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'auth_date': int(time.time()),  # Время запроса
    }
    secret_key = hmac.new(
        BOT_TOKEN.encode('utf-8'),
        b'Telegram',
        hashlib.sha256
    ).digest()
    data_check_string = '\n'.join(f'{k}={v}' for k, v in sorted(user_data.items()))
    user_data['hash'] = hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Отправляем запрос на сайт
    try:
        response = requests.post(BASE_URL, data=user_data)
        response.raise_for_status()  # Проверка кода состояния ответа
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        await message.answer("Не удалось связаться с сервером. Попробуйте позже.")
        return

    # Обработка ответа
    if response.status_code == 200:
        # Сохранение данных пользователя
        if db_pool:
            try:
                await create_user(db_pool, user_data)
            except Exception as e:
                print(f"Не удалось сохранить данные пользователя: {e}")
        await message.answer('Вы успешно авторизовались на сайте!')
    else:
        await message.answer('Не удалось авторизоваться. Попробуйте снова.')
