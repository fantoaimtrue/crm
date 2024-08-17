from django.urls import path
from .views import edit_profile, view_profile

app_name = 'profile'


urlpatterns = [
    path('edit/', edit_profile, name='edit_profile'),
    path('view/', view_profile, name='view_profile'),

]