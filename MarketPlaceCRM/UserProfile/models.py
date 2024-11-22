# models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(null=True, blank=True)  # Поле email
    wb_token = models.TextField(null=True, blank=True)  # Поле wb_token
    ozon_token = models.TextField(null=True, blank=True)  # Поле ozon_token
    ozon_client_id = models.IntegerField(null=True, default=0)  # Поле ozon_client_id
    tg_username = models.TextField(null=True, blank=True)  # Telegram username
    tg_first_name = models.TextField(null=True, blank=True)  # Telegram first name
    tg_last_name = models.TextField(null=True, blank=True)  # Telegram last name
    telegram_id = models.BigIntegerField(unique=True, null=True)# Telegram ID

    def __str__(self):
        return self.user.username
    
  

    