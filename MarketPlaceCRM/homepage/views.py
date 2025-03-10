from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  # Добавьте этот импорт
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from UserProfile.models import Profile
from .models import TelegramAuthLog
import logging

import hashlib
import hmac
import time
from decouple import config


logger = logging.getLogger(__name__)
BOT_TOKEN = config("BOT_TOKEN")


def check_telegram_auth(data):
    logger.debug(f"Incoming data for auth: {data}")
    """Проверяем подлинность данных от Telegram"""
    required_keys = ["auth_date", "hash", "id"]
    if not all(key in data for key in required_keys):
        return False

    bot_token = BOT_TOKEN
    auth_date = int(data["auth_date"])
    current_time = time.time()

    # Проверка срока действия данных
    if current_time - auth_date > 86400:  # 1 день
        return False

    # Проверка повторного использования данных (Replay-атака)
    telegram_id = data.get("id")
    if is_replay_attack(auth_date, telegram_id):
        return False

    # Формирование строки для проверки
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()) if k != "hash")
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hash_hex = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

    # Сравнение хэшей
    if hash_hex != data["hash"].lower():
        return False

    return True


def is_replay_attack(auth_date, telegram_id):
    """Проверка на повторное использование данных авторизации"""
    # Ищем запись с таким же auth_date и telegram_id
    if TelegramAuthLog.objects.filter(
        telegram_id=telegram_id, auth_date=auth_date
    ).exists():
        return True

    # Создаем запись в базе
    TelegramAuthLog.objects.create(telegram_id=telegram_id, auth_date=auth_date)
    return False


def telegram_login(request):
    """Обработка данных из виджета Telegram"""
    if check_telegram_auth(request.GET):
        telegram_id = request.GET.get("id")  # Получаем telegram_id
        first_name = request.GET.get("first_name")
        username = request.GET.get("username")

        if not telegram_id:
            return JsonResponse({"error": "Telegram ID not provided"}, status=400)

        # Поиск или создание пользователя
        user, created = User.objects.get_or_create(
            username=username, defaults={"first_name": first_name}
        )

        # Проверка, существует ли уже профиль с таким telegram_id
        profile, profile_created = Profile.objects.get_or_create(user=user)

        # Проверяем, если профиль создан, то нужно установить telegram_id
        if profile_created:
            profile.telegram_id = telegram_id

        # Обновляем профиль и сохраняем его
        profile.tg_username = username
        profile.save()

        # Выполняем аутентификацию
        login(request, user)

        print("Пользователь успешно аутентифицирован")  # Для отладки
        return redirect("main:homepage")  # Перенаправление на главную страницу
    print("Данные Telegram недействительны")  # Для отладки
    return JsonResponse({"error": "Invalid Telegram data"}, status=400)


# Кастомная форма аутентификации
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


# Авторизация через форму
def login_request(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Проверка и создание профиля
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    profile = Profile.objects.create(user=user)

                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = CustomAuthenticationForm()
    return render(
        request=request, template_name="auth/login.html", context={"login_form": form}
    )


# Выход из системы
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


# Домашняя страница
@login_required
def homepage(request):
    context = {"Content": "content"}
    return render(request, "homepage/homepage.html", context)
