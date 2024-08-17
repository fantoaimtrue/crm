# models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(null=True)
    wb_token = models.TextField(null=True)
    ozon_token = models.TextField(null=True)
    telegram_id = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username
    
  

    