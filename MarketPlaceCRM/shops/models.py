from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField


class ShopCard(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.TextField(
        max_length=200, unique=True, verbose_name='Название магазина')
    shop_wb_token = EncryptedCharField(max_length=255, null=True, blank=True)
    shop_ozon_token = EncryptedCharField(max_length=255, null=True, blank=True)
    shop_ozon_client_id = EncryptedCharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = 'shop_card'
