from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=False 
    )

    class Meta:
        model = Profile
        fields = ['email', 'wb_token', 'ozon_token', 'tg_username']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите свой email адрес'}
            ),
            'wb_token': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите токен wb'}
            ),
            'ozon_token': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите токен ozon'}
            ),
            'tg_username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите свое имя в Telegram в формате "@username"'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user_name'].initial = user.get_full_name() or user.username
