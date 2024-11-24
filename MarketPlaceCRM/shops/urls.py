from django.urls import path
from .views import view_shop, edit_shops_card, add_shops, delete_shop


app_name = "shops"


urlpatterns = [
    path("view_shops/", view_shop, name="view_shops"),
    path("edit_shops/<int:id>/", edit_shops_card, name="edit_shops"),
    path("add_shops/", add_shops, name="add_shops"),
    path("delete_shop/<int:id>/", delete_shop, name="delete_shop"),
]
