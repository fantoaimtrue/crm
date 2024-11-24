from django import forms
from .models import ShopCard
from django.forms import ModelForm


class ShopCardForm(ModelForm):
    class Meta:
        model = ShopCard
        fields = ['shop_name', 'shop_wb_token', 'shop_ozon_token', 'shop_ozon_client_id']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название магазина'}),
            'shop_wb_token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите токен от WB'}),
            'shop_ozon_token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите токен от OZON'}),
            'shop_ozon_client_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите client-id от OZON'}),
            
        }
