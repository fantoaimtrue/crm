from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import csv
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UploadCSVForm, ProductCardForm
from .models import ProductCard


@login_required
def add_product(request):
    return render(request, 'products/add_product.html')

@login_required
def add_product_alone(request):
    if request.method == 'POST':
        form = ProductCardForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products:view_products')
    else:
        form = ProductCardForm()
    return render(request, 'products/add_product_alone.html', {'form': form})



@login_required
def add_product_from_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            csv_content = csv_file.read().decode('utf-8-sig')
            reader = csv.DictReader(csv_content.splitlines(), delimiter=';')

            # Обработка данных
            for row in reader:
                name = row.get('Артикул', '').strip('"').strip("'")
                price = row.get('Текущая цена с учетом скидки, ₽', '').strip('"').strip("'")
                weight = row.get('Объемный вес, кг', '').strip('"').strip("'")

                # Замена запятой на точку для корректного преобразования в float
                price = price.replace(',', '.')
                weight = weight.replace(',', '.')
                
                

                # Проверка наличия всех необходимых полей
                if name and price and weight:
                    try:
                        price = float(price)  # Преобразуем цену в число с плавающей точкой
                        weight = float(weight)  # Преобразуем вес в число с плавающей точкой
                    except ValueError:
                        messages.warning(request, f'Неверные данные в строке: {row}')
                        continue

                    # Проверяем, существует ли уже товар с таким названием
                    user = request.user
                    if not ProductCard.objects.filter(product_name=name).exists():
                        ProductCard.objects.create(
                            user=user,
                            product_name=name,
                            product_price=price,
                            product_weight=weight
                        )
                else:
                    messages.warning(request, f'Недостаточные данные в строке: {row}')
                    print('Недостаточно данных в строке')
                    
            messages.success(request, 'Товары успешно добавлены.')
            return redirect(reverse('products:view_products'))
    else:
        form = UploadCSVForm()
        print(form.errors)
        
    return render(request, 'products/add_product_from_csv.html', {'form': form})



@login_required
def view_products(request):
    all_products = ProductCard.objects.filter(user=request.user)
    column_names = ['Выбрать объект', 'Имя товара', 'Цена товара', 'Вес товара']
    
    if not all_products.exists():
        return redirect('products:add_product')

    context = {
        'products': all_products,
        'column_names': column_names
    }
    return render(request, 'products/view_products.html', context)


@login_required
def edit_product_card(request, id):
    product = get_object_or_404(ProductCard, pk=id)
    if request.method == "POST":
        form = ProductCardForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Перенаправляем на страницу со списком товаров после успешного редактирования
            return redirect('products:view_products')
    else:
        form = ProductCardForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'data': product})

@login_required
def delete_product(request, id):
    product = get_object_or_404(ProductCard, pk=id)
    if request.method == 'POST':
        product.delete()
        return redirect('products:view_products')
    return render(request, 'products/delete_product.html', {'product': product})



