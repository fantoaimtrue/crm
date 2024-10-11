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


# headers = {
#     'Authorization': wb_aqua_api_key,
# }

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d")



# Функция для получения всех данных статистики и сохранения их в JSON файлы
def get_all_statics(date):
    urls = {
        'sales': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
    }
    data = {}
    for url_key, link in urls.items():
        response = requests.get(url=link, headers={'Authorization': wb_aqua_api_key}, params={
            'dateFrom': date,
        })
        if response.status_code == 200:
            data[url_key] = response.json()
            with open(f'parser/reports/wb/{url_key}.json', 'w', encoding='utf-8') as f:
                json.dump(data[url_key], f, ensure_ascii=False, indent=4)
        else:
            pprint(f'Не удалось получить данные с {link}. Код состояния: {response.status_code}')
    return data

# Функция для сбора всех продаж за указанный месяц и год
def all_sales(api_key, sales_year, sales_month, date):
    url = 'https://statistics-api.wildberries.ru/api/v1/supplier/sales'
    headers = {
        'Authorization': api_key
    }
    params = {
        'dateFrom': date
    }
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()  # Преобразуем ответ в JSON
    else:
        print(f"Error: {response.status_code}")
    if not data:
        print("No data found")
        return

    all_items = {}
    for c in data:
        try:
            
            if c['forPay'] > 0:
                date_str = c['date'][:10]
                current_year, month = date_str.split('-')[:2]
                if current_year == sales_year and month == sales_month:
                    if 'supplierArticle' in c:
                        key = c['supplierArticle']
                        if key not in all_items:
                            all_items[key] = {
                                "mid_price": [],
                                "qty": 0,
                            }
                        all_items[key]['mid_price'].append(c['forPay'])
                        all_items[key]['qty'] += 1
                    else:
                        print("Missing supplierArticle in item.")
        except Exception as ex:
            pprint(f'ОШИБКА: {ex}')


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
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "wb",
                                f"wb_{date}.xlsx")
        df.to_excel(report_path, index=False)
        print(f"Готово! Файл отчета с WB создан. End array length: {len(end_arr)}")


   
# Основная функция
def main():
    all_sales(sales_year='2024', sales_month='08', date='2024-08')
    # test_wb(date='2024-2', brand='sec_of_chameleon', label='Секреты Хамелеона')
    # get_all_statics(date='2024-08')
if __name__ == '__main__':
    main()
