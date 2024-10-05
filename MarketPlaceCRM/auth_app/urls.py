from django.urls import path
from .views import telegram_login

app_name = 'auth_app'  # Указываем имя приложения

urlpatterns = [
    path('telegram/login/', telegram_login, name='telegram_login'),
]