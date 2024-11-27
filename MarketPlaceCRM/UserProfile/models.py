# models.py
from django.contrib.auth.models import User
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(null=True, blank=True)  # Поле email
    tg_username = models.TextField(null=True, blank=True)  # Telegram username
    tg_first_name = models.TextField(null=True, blank=True)  # Telegram first name
    tg_last_name = models.TextField(null=True, blank=True)  # Telegram last name
    telegram_id = models.BigIntegerField(unique=True, null=True)# Telegram ID

    def __str__(self):
        return self.user.username
    
  

    