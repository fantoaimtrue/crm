from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from UserProfile.models import Profile
import hashlib
import hmac
import time
from django.conf import settings

def check_telegram_auth(data):
    """Проверяем подлинность данных от Telegram"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    auth_date = int(data.get('auth_date', 0))
    current_time = time.time()

    # Проверка, что данные от Telegram актуальны (менее 1 дня)
    if current_time - auth_date > 86400:  # 1 день
        return False

    # Формируем строку для проверки подписи
    check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items()) if k != 'hash'])
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hash_hex = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

    # Проверяем, совпадает ли хэш
    if hash_hex != data.get('hash'):
        return False

    return True


def telegram_login(request):
    """Обработка данных из виджета Telegram"""
    print(request.GET)  # Выводим данные для отладки
    if check_telegram_auth(request.GET):
        telegram_id = request.GET.get('id')
        first_name = request.GET.get('first_name')
        username = request.GET.get('username')

        # Создание пользователя или получение существующего
        user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name})

        # Создание или обновление профиля
        profile, profile_created = Profile.objects.get_or_create(user=user)
        profile.tg_username = username
        profile.save()

        # Вход пользователя и создание сессии
        login(request, user)

        # Перенаправление на главную страницу после успешного входа
        return redirect('main:homepage')  # Или куда вам нужно
    else:
        # В случае ошибки Telegram-данных
        return JsonResponse({'error': 'Invalid Telegram data'}, status=400)
