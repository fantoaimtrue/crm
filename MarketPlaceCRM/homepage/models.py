from django.db import models

# Create your models here.
class TelegramAuthLog(models.Model):
    telegram_id = models.CharField(max_length=50, unique=False)  # Telegram ID пользователя
    auth_date = models.BigIntegerField()  # Время авторизации (UNIX timestamp)
    created_at = models.DateTimeField(auto_now_add=True)  # Когда запись была добавлена

    class Meta:
        unique_together = ('telegram_id', 'auth_date')  # Гарантия уникальности
        indexes = [
            models.Index(fields=['telegram_id', 'auth_date']),
        ]