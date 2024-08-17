from django import forms
from .models import Report
from django.forms import ModelForm, modelformset_factory


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['product_name', 'price_uan',
                  'product_weight', 'product_quantity']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя товара'}),
            'product_price': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите цену товара (в Юанях)'}),
            'product_weight': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите вес товара (в кг)'}),
            'product_quantity': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите кол-во товара'}),
        }


class ReportCardForm(ModelForm):
    class Meta:
        model = Report
        fields = [
            'product_name',
            'price_uan',
            'price_rub',
            'delivery_in_china_uan',
            'delivery_in_china_rub',
            'commission_uan',
            'commission_rub',
            'delivery_to_moscow',
            'delivery_to_office',
            'last_insurance'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя товара'}),
            'price_uan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена товара (в Юанях)'}),
            'price_rub': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена товара (в Рублях)'}),
            'delivery_in_china_uan': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Доставка до китая в юанях.'}),
            'delivery_in_china_rub': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Доставка до китая в рублях.'}),
            'commission_uan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Комиссия в юанях.'}),
            'commission_rub': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Комиссия в рублях.'}),
            'delivery_to_moscow': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Доставка до Москвы'}),
            'delivery_to_office': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Доставка до офиса'}),
            'last_insurance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Страховка'})
        }


ReportFormSet = modelformset_factory(Report, form=ReportCardForm, extra=0)
