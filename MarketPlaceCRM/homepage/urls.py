from django.urls import path
from .views import login_request, logout_view, homepage, telegram_login

app_name = 'main'

urlpatterns = [
    path('', login_request, name='login'),  # Страница входа через форму
    path('homepage/', homepage, name='homepage'),  # Домашняя страница
    path('logout/', logout_view, name='logout'),  # Выход из системы
    path('telegram/login/', telegram_login, name='telegram_login'),  # Вход через Telegram
]
