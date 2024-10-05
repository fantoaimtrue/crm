import hashlib
import hmac
import time
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from UserProfile.models import Profile

def check_telegram_auth(data):
    """Проверяем подлинность данных от Telegram"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    auth_date = int(data.get('auth_date', 0))
    current_time = time.time()

    if current_time - auth_date > 86400:  # 1 день
        return False

    check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items()) if k != 'hash'])
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hash_hex = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

    if hash_hex != data.get('hash'):
        return False

    return True

def telegram_login(request):
    """Обработка данных из виджета Telegram"""
    if check_telegram_auth(request.GET):
        telegram_id = request.GET.get('id')
        first_name = request.GET.get('first_name')
        username = request.GET.get('username')

        # Поиск или создание пользователя
        user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name})
        
        # Поиск или создание профиля пользователя
        profile, profile_created = Profile.objects.get_or_create(user=user)
        
        # Обновляем информацию в профиле, если нужно
        profile.tg_username = username
        profile.save()
        
        # Выполняем аутентификацию
        login(request, user)
        return redirect('auth/login.html')  # Перенаправляем пользователя на главную страницу или другую
    return JsonResponse({'error': 'Invalid Telegram data'}, status=400)
