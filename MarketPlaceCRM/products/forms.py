from django import forms
from .models import ProductCard
from django.forms import ModelForm


class ProductCardForm(ModelForm):
    class Meta:
        model = ProductCard
        fields = ['product_name', 'product_price', 'product_weight']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя товара'}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену товара (в Юанях)'}),
            'product_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите вес товара (в кг)'}),
            # 'product_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество товара'}),
        }


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()