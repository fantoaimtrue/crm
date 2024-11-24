from django.shortcuts import render

# Create your views here.
from pprint import pprint

from django.template import context
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ShopCardForm
from .models import ShopCard


@login_required
def view_shop(request):
    all_products = ShopCard.objects.filter(user=request.user)
    column_names = ['Имя магазина', 'WB-токен', 'OZON-токен', 'OZON client-id']
    
    if not all_products.exists():
        return redirect('shops:add_shops')

    context = {
        'shops': all_products,
        'column_names': column_names
    }
    return render(request, 'shops/shops.html', context)


@login_required
def add_shops(request):
    if request.method == 'POST':
        form = ShopCardForm(request.POST)
        if form.is_valid():
            shops = form.save(commit=False)
            shops.user = request.user
            shops.save()
            return redirect('shops:view_shops')
    else:
        form = ShopCardForm()
    return render(request, 'shops/add_shops.html', {'form': form})


@login_required
def edit_shops_card(request, id):
    shops = get_object_or_404(ShopCard, pk=id)
    if request.method == "POST":
        form = ShopCardForm(request.POST, instance=shops)
        if form.is_valid():
            form.save()
            # Перенаправляем на страницу со списком товаров после успешного редактирования
            return redirect('shops:view_shops')
    else:
        form = ShopCardForm(instance=shops)
    return render(request, 'shops/edit_shops.html', {'form': form, 'data': shops})


@login_required
def delete_shop(request, id):
    shop = get_object_or_404(ShopCard, pk=id)
    if request.method == 'POST':
        shop.delete()
        return redirect('shops:view_shops')
    return render(request, 'shops/delete_shop.html', {'shop': shop})