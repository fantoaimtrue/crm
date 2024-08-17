from pprint import pprint

from django.template import context
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import ProductCard
from .models import Report, Reports
from .forms import ReportFormSet
from products.views import view_products


@login_required
def generate_report(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        selected_items_int = [int(item) for item in selected_items]  # Достаем из чекбоксов ID наших товаров и добавляем их в список
        # Фильтруем только те товары, которые принадлежат текущему пользователю
        selected_objects = ProductCard.objects.filter(id__in=selected_items_int, user=request.user)
        context = {
            'objects': selected_objects
        }

        return render(request, 'reports/generate_report.html', context)
    else:
        # Дополнительный код на случай GET-запроса, если требуется
        pass


@login_required
def save_report(request):
    if request.method == 'POST':
        price_prefix = 'product_price_'
        quantity_prefix = 'product_quantity_'
        name_prefix = 'product_name_'
        weight_prefix = 'product_weight_'
        delivery_prefix = 'delivery_in_china_'

        product_prices = {}
        product_quantities = {}
        product_names = {}
        product_weights = {}
        deliverys_in_china = {}

        try:
            for key in request.POST:
                if key.startswith(price_prefix):
                    product_id = key[len(price_prefix):]
                    product_prices[product_id] = float(request.POST[key].replace(',', '.'))
                elif key.startswith(quantity_prefix):
                    product_id = key[len(quantity_prefix):]
                    product_quantities[product_id] = int(request.POST[key])
                elif key.startswith(name_prefix):
                    product_id = key[len(name_prefix):]
                    product_names[product_id] = request.POST[key]
                elif key.startswith(weight_prefix):
                    product_id = key[len(weight_prefix):]
                    product_weights[product_id] = float(request.POST[key].replace(',', '.'))
                elif key.startswith(delivery_prefix):
                    product_id = key[len(delivery_prefix):]
                    deliverys_in_china[product_id] = float(request.POST[key].replace(',', '.'))
        except ValueError as e:
            return JsonResponse({'error': f'Неверный формат данных: {str(e)}'}, status=400)

        try:
            commission = float(request.POST.get('commission', '0').replace(',', '.'))
            commission_5_proc = {
                product_id: (product_prices[product_id]) * commission / 100
                for product_id in product_prices
            }
        except ValueError as e:
            return JsonResponse({'error': f'Неверная комиссия: {str(e)}'}, status=400)

        try:
            purchase_amount = sum(
                product_prices[product_id] * product_quantities[product_id]
                for product_id in product_prices
            )
        except ValueError as e:
            return JsonResponse({'error': f'Неверная сумма покупки: {str(e)}'}, status=400)

        total_weight = sum(
            product_weights.get(product_id, 0) * product_quantities.get(product_id, 0)
            for product_id in product_weights
        )

        try:
            delivery_office = float(request.POST.get('delivery_to_office', '0').replace(',', '.'))
            delivery_moscow = float(request.POST.get('delivery_to_moscow', '0').replace(',', '.'))
        except ValueError as e:
            return JsonResponse({'error': f'Неверная стоимость доставки в офис или Москву: {str(e)}'}, status=400)

        reports_instance = Reports.objects.create(user=request.user)  # Привязка отчета к пользователю

        for product_id in product_prices:
            try:
                insurance = float(request.POST.get('last_insurance', '0').replace(',', '.'))
                course_dollar = float(request.POST.get('price_dollar', 0))
                course_uan = float(request.POST.get('price_uan', 0))

                price_uan = product_prices[product_id]
                price_rub = price_uan * course_uan
                commission = commission_5_proc.get(product_id, 0)
                quantity = product_quantities.get(product_id, 0)
                weight = product_weights.get(product_id, 0)
                div_in_china = deliverys_in_china.get(product_id, 0) / quantity
                delivery_to_office_item = (weight * delivery_office) / total_weight if total_weight != 0 else 0
                delivery_to_moscow_item = (weight * delivery_moscow) / total_weight if total_weight != 0 else 0

                last_insurance = (price_rub + round(div_in_china * course_uan, 2) + commission * course_uan) * insurance / 100

                report_instance = Report(
                    rep=reports_instance,
                    product_name=product_names.get(product_id),
                    price_uan=price_uan,
                    price_rub=price_rub,
                    product_weight=weight,
                    product_quantity=quantity,
                    delivery_in_china_uan=round(div_in_china, 2),
                    delivery_in_china_rub=round(div_in_china, 2) * course_uan,
                    commission_uan=commission,
                    commission_rub=commission * course_uan,
                    delivery_to_moscow=delivery_to_moscow_item * course_dollar,
                    delivery_to_office=delivery_to_office_item,
                    last_insurance=last_insurance
                )
                report_instance.save()
            except ValueError as e:
                return JsonResponse({'error': f'Ошибка в расчетах: {str(e)}'}, status=400)

        return redirect('reports:view_reports')
    else:
        # Дополнительный код на случай GET-запроса, если требуется
        return render(request, 'reports/save_report.html')



@login_required
def view_reports(request):
    # Фильтрация отчетов текущего пользователя
    reports = Reports.objects.filter(user=request.user)

    # Фильтрация продуктов текущего пользователя
    products = ProductCard.objects.filter(user=request.user)

    #Проверка на наличие данных в базе
    if not reports.exists() or not products.exists():
        return redirect('products:view_products')

    context = {
        'reports': reports,
        'products': products
    }
    return render(request, 'reports/view_reports.html', context)


@login_required
def view_report(request, report_id):
    reports_instance = get_object_or_404(Reports, pk=report_id)
    reports = Report.objects.filter(rep=reports_instance)

    if request.method == 'POST':
        formset = ReportFormSet(request.POST, queryset=reports)
        if formset.is_valid():
            formset.save()
            return redirect('reports:view_report', report_id=report_id)
    else:
        formset = ReportFormSet(queryset=reports)

    titles = [
        'Название товара',
        "Цена в Юанях",
        "Цена в Рублях",
        "Доставка по Китаю в Юанях",
        "Доставка по Китаю в Рублях",
        "Комиссия в Юанях",
        "Комиссия в Рублях",
        "Доставка до Москвы",
        "Доставка до Офиса",
        "Страховка",
    ]

    context = {
        'formset': formset,
        'titles': titles,
        'reports': reports,
        'report_id': report_id,
        'report_instance': reports_instance,
    }

    return render(request, 'reports/view_report.html', context)


@login_required
def download_report(request, report_id):
    reports = Report.objects.filter(rep_id=report_id)

    data = []
    for report in reports:
        data.append([
            report.product_name, report.price_uan, report.price_rub,
            report.delivery_in_china_uan, report.delivery_in_china_rub,
            report.commission_uan, report.commission_rub,
            report.delivery_to_moscow, report.delivery_to_office,
            report.last_insurance
        ])

    df = pd.DataFrame(data,
                      columns=['Имя продукта', 'Цена за единицу товара (¥)', 'Цена за единицу товара (₽)',
                               'Доставка по Китаю (¥)', 'Доставка по Китаю (₽)', 'Комиссия (¥)', 'Комиссия (₽)',
                               'Доставка до МСК (₽)', 'Доставка до офиса (₽)', 'Страховка (₽)'])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=report_{report_id}.xlsx'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response


@login_required
def delete_report(request, report_id):
    report_instance = get_object_or_404(Reports, id=report_id)
    report_instance.delete()
    return redirect('reports:view_reports')
