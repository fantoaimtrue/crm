from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from UserProfile.models import Profile
from django.shortcuts import render


# Авторизация
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


## Вход в систему
def login_request(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Проверка и создание профиля
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    profile = Profile.objects.create(user=user)
                
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('main:homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    
    form = CustomAuthenticationForm()
    return render(request=request, template_name="auth/login.html", context={"login_form": form})


## Выход из системы
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


# Домашняя страница
@login_required
def homepage(request):
    context = {
        "Content": 'content'
    }
    return render(request, "homepage/homepage.html", context)
