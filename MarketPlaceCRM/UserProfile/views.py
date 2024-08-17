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
