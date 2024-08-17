# simpleapp/urls.py
from django.urls import path
from .views import login_request, logout_view, homepage


app_name = 'main'


urlpatterns = [
    path('', login_request, name='login'),
    path('homepage/', homepage, name='homepage'),
    path('logout/', logout_view, name='logout'),
]
