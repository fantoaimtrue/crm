from django.db import models
from django.contrib.auth.models import User


class ProductCard(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.TextField(
        max_length=200, unique=True, verbose_name='Имя товара')
    product_price = models.FloatField(verbose_name='Цена товара')
    product_weight = models.FloatField(verbose_name='Вес товара')
    delivery_in_china = models.FloatField(verbose_name='Доставка по Китаю', default=0)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_card'
