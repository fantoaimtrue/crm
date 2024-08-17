from django.urls import path
from .views import add_product_from_csv, add_product_alone, edit_product_card, delete_product, view_products, add_product


app_name = 'products'


urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('add_product_alone/', add_product_alone, name='add_product_alone'),
    path('add_product_from_csv/', add_product_from_csv, name='add_product_from_csv'),
    path('view_products/', view_products, name='view_products'),
    path('edit_product/<int:id>/', edit_product_card, name='edit_product'),
    path('delete_product/<int:id>/', delete_product, name='delete_product'),
]
