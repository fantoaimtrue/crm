from django.db import models
from django.contrib.auth.models import User


class ShopCard(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_name = models.TextField(
        max_length=200, unique=True, verbose_name='Название магазина')
    shop_wb_token = models.TextField(verbose_name='WB-token')
    shop_ozon_token = models.TextField(verbose_name='OZON-token')
    shop_ozon_client_id = models.TextField(verbose_name='OZON-client-id', default=0)
    
    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = 'shop_card'
