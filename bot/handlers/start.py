from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
# from db import create_user
from keyboards.default import kb_report
from decouple import config, Csv


router = Router()

# Инициализация подключения к БД
# db_pool = None


BOT_TOKEN = config('BOT_TOKEN')
BASE_URL = 'https://crmmarketplacehelper.ru/telegram_login/'

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
    response = requests.post(BASE_URL, data=user_data)
    if response.status_code == 200:
        await message.answer('Вы успешно авторизовались на сайте!')
    else:
        await message.answer('Не удалось авторизоваться. Попробуйте снова.')
