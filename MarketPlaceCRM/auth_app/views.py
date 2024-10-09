import hashlib
import hmac
import time
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from UserProfile.models import Profile
from django.http import HttpResponse

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
    if check_telegram_auth(request.GET):
        telegram_id = request.GET.get('id')
        first_name = request.GET.get('first_name')
        username = request.GET.get('username')

        user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name})
        profile, profile_created = Profile.objects.get_or_create(user=user)
        profile.tg_username = username
        profile.save()

        login(request, user)
        
        return HttpResponse("Login successful", status=200)  # Возвращаем простой текстовый ответ
    
    return HttpResponse("Invalid Telegram data", status=400)
