from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile:view_profile')  # Убедитесь, что это имя соответствует вашему URL
        else:
            # Можно передать ошибки в шаблон для отображения
            print(form.errors)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile/edit_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = request.user.profile  # Получение профиля пользователя
    return render(request, 'profile/view_profile.html', {'profile': profile})



from django.contrib.auth.models import User
from .models import Profile

# Функция для создания или обновления профиля пользователя в Django
async def create_user(user_data: dict):
    try:
        # Получаем или создаем пользователя в Django (если его нет)
        user, created = User.objects.get_or_create(username=user_data['username'])

        # Создаем или обновляем профиль пользователя
        profile, created = Profile.objects.get_or_create(user=user)

        # Обновляем или устанавливаем данные профиля
        profile.tg_username = user_data['username']
        profile.tg_first_name = user_data['first_name']
        profile.tg_last_name = user_data['last_name']
        profile.telegram_id = user_data['id']
        profile.email = user_data.get('email', None)  # Если email есть, то обновим
        profile.save()

    except Exception as e:
        print(f"Ошибка при создании/обновлении пользователя: {e}")
        raise Exception("Ошибка при сохранении данных пользователя в базе данных.")
