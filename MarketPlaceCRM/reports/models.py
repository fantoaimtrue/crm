from django.db import models

from products.models import ProductCard
from django.contrib.auth.models import User


class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='Alex')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату в строку


class Report(models.Model):
    rep = models.ForeignKey(Reports, on_delete=models.CASCADE, related_name='reports')
    product_name = models.CharField(max_length=255, verbose_name='name')
    price_uan = models.FloatField(default=0, verbose_name='price_uan')
    price_rub = models.FloatField(default=0, verbose_name='price_rub')
    product_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='weight')
    product_quantity = models.IntegerField(default=0, verbose_name='quantity')
    delivery_in_china_uan = models.FloatField(default=0, verbose_name='delivery_in_china_uan')
    delivery_in_china_rub = models.FloatField(default=0, verbose_name='delivery_in_china_rub')
    commission_uan = models.FloatField(verbose_name='commission_uan')
    commission_rub = models.FloatField(verbose_name='commission_rub')
    delivery_to_moscow = models.FloatField(default=0, verbose_name='delivery_to_moscow')
    delivery_to_office = models.FloatField(default=0, verbose_name='delivery_to_office')
    last_insurance = models.FloatField(default=0, verbose_name='last_insurance')

    def __str__(self):
        return self.product_name


