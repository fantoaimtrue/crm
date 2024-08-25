import json
import os
from datetime import datetime
import pandas as pd
import requests
from datetime import datetime
from pprint import pp, pprint
from dotenv import load_dotenv

load_dotenv()
wb_aqua_api_key = str(os.getenv('WB_AQUA_API_KEY'))

# Настройка заголовков и параметров для API запроса
#test branch




current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d")



# # Функция для получения всех данных статистики и сохранения их в JSON файлы
# def get_all_statics(date):
#     urls = {
#         'sales': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
#     }
#     data = {}
#     for url_key, link in urls.items():
#         response = requests.get(url=link, headers=headers, params={
#             'dateFrom': date,
#         })
#         if response.status_code == 200:
#             data[url_key] = response.json()
#         else:
#             pprint(f'Не удалось получить данные с {link}. Код состояния: {response.status_code}')
#     return data
#     print(data)

# Функция для сбора всех продаж за указанный месяц и год
def all_sales(sales_year, sales_month, label, brand, date):
    headers = {
        'Authorization': wb_aqua_api_key,
    }
    response = requests.get(url='https://statistics-api.wildberries.ru/api/v1/supplier/sales', headers=headers, params={
            'dateFrom': date,
        }).json()
    data = response.get('sales', [])
    if not data:
        print("No data found")
        return

    all_items = {}
    for c in data:
        try:
            print(f"Processing item: {c}")
            if c['brand'] == label:
                print(f"Brand matches: {c['brand']}")
                if c['forPay'] > 0:
                    print(f"ForPay > 0: {c['forPay']}")
                    date_str = c['date'][:10]
                    current_year, month = date_str.split('-')[:2]
                    print(f"Year: {current_year}, Month: {month}")
                    if current_year == sales_year and month == sales_month:
                        print(f"Year and month match: {current_year}-{month}")
                        if 'supplierArticle' in c:
                            key = c['supplierArticle']
                            if key not in all_items:
                                all_items[key] = {
                                    "mid_price": [],
                                    "qty": 0,
                                }
                            all_items[key]['mid_price'].append(c['forPay'])
                            all_items[key]['qty'] += 1
                            print(f"Updated all_items: {all_items}")
                        else:
                            print("Missing supplierArticle in item.")
        except Exception as ex:
            pprint(f'ОШИБКА: {ex}')

    print(f"All items collected: {all_items}")

    end_arr = []
    for key, value in all_items.items():
        full = sum(value['mid_price'])
        mid_price = full / value['qty']
        end_arr.append({
            'Товар': key,
            'Средняя цена': mid_price,
            'Количество': value['qty'],
            'Продано на': full
        })

    if not end_arr:
        print("End array is empty.")
    else:
        df = pd.DataFrame(data=end_arr)
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"reports/wb/{'aqua' if label == 'Секреты Хамелеона' else 'csc'}/wb_{brand}_{date}.xlsx")
        df.to_excel(report_path, index=False)
        print(f"Готово! Файл отчета с WB создан. End array length: {len(end_arr)}")


# Функция для тестирования сбора данных с WB
def test_wb(date, brand, label):
    data = get_all_statics().get('sales', [])
    if not data:
        return

    arr = {}
    plot = 0
    for r in data:
        if r.get('return_amount', 0) == 0 and r.get('brand_name') == label:
            if r.get('sa_name') == 'плот_большой':
                plot += 1
            sa_name = r.get('sa_name')
            if sa_name not in arr:
                arr[sa_name] = {
                    'qty': 0,
                    'sale_sum': 0,
                    'commission_sum': 0,
                    'prices': []
                }

            retail_amount = r.get('retail_amount', 0)
            quantity = r.get('quantity', 0)
            commission_percent = r.get('commission_percent', 0)
            delivery_rub = r.get('delivery_rub', 0) or 0

            arr[sa_name]['qty'] += quantity
            arr[sa_name]['sale_sum'] += retail_amount * quantity
            arr[sa_name]['commission_sum'] += (retail_amount * quantity * commission_percent) + delivery_rub
            if retail_amount > 0:
                arr[sa_name]['prices'].append({'price': retail_amount, 'qty': quantity})

    for a in arr.values():
        sum_prices = sum(p['price'] * p['qty'] for p in a['prices'])
        total_qty = sum(p['qty'] for p in a['prices'])
        a['mid_price'] = round(sum_prices / total_qty, 2) if total_qty else 0

    end_arr = [{
        'Товар': a,
        'Средняя цена': arr[a]['mid_price'],
        'Количество': arr[a]['qty'],
        'Продано на': arr[a]['sale_sum'],
        'Сумма комиссий WB': arr[a]['commission_sum'],
        'Оборот с учетом комиссии WB': arr[a]['sale_sum'] - arr[a]['commission_sum'],
    } for a in arr]

    df = pd.DataFrame(data=end_arr)
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"reports/wb/{'aqua' if brand == 'sec_of_chameleon' else 'csc'}/wb_{date}.xlsx")
    df.to_excel(report_path, index=False)
    print("Готово! Файл отчета с WB создан.")

# Основная функция
def main():
    all_sales(sales_year='2024', sales_month='08', label='Секреты Хамелеона', brand='sec_of_chameleon', date='2024-08')
    # test_wb(date='2024-2', brand='sec_of_chameleon', label='Секреты Хамелеона')

if __name__ == '__main__':
    main()
