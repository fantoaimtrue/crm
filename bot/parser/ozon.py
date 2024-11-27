import json
import os
from calendar import monthrange
from pprint import pp, pprint
from urllib import response

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


aqua_api_key = str(os.getenv('AQUA_API_KEY'))
aqua_client_id = str(os.getenv('AQUA_CLIENT_ID'))

csc_api_key = str(os.getenv('CSC_API_KEY'))
csc_client_id = str(os.getenv('CSC_CLIENT_ID'))

def cfg(config):
    if config == 'sec_of_chameleon':
        api_key = aqua_api_key
        client_id = aqua_client_id
        return api_key, client_id
    elif config == 'cscgaming':
        api_key = csc_api_key
        client_id = csc_client_id
        return api_key, client_id
    else:
        return None


def ozon(config, method, data):
    cf = cfg(config)
    headers = {'Api-Key': cf[0], 'Client-Id': cf[1], 'Content-Type': 'application/json'}
    response = requests.post("https://api-seller.ozon.ru/" + method, headers=headers, json=data)
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()


def get_data_ozon(client_id, api_key):
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    get_url = "https://api-seller.ozon.ru/v2/analytics/stock_on_warehouses"
    json_data = {
        "limit": 1000,
        "offset": 0,
        "warehouse_type": "ALL"
    }
    resp_data = requests.post(get_url, headers=headers, json=json_data).json()
    remainder = {}
    list_warehouse = resp_data['result']['rows']
    for n in list_warehouse:
        item_code = n['item_code']
        free_to_sell_amount = n['free_to_sell_amount']
        remainder[item_code] = free_to_sell_amount
    return remainder



def report(api_key, client_id, month, year):
    # cf = cfg(config)
    # if not cf:
    #     return

    arr = dict()
    headers = {'Api-Key': str(api_key), 'Client-Id': str(client_id), 'Content-Type': 'application/json'}
    response = requests.post("https://api-seller.ozon.ru/" + 'v2/finance/realization', headers=headers, json={"month": month,
                                                  "year": year})
    response.raise_for_status()  # Raises an error for bad responses
    res = response.json()
    # res = ozon(config, 'v2/finance/realization', {"month": month,
    #                                               "year": year})
    
    # if res.get('message'):
    #     return

    for r in res['result']['rows']:
        item_name = r['item']['offer_id']
        item_price = r['seller_price_per_instance']
        commission_ratio = r['commission_ratio'] 
        if r['delivery_commission'] is not None:
            item_qty = r['delivery_commission']['quantity']

        if item_name:
            if item_name not in arr:
                # даем имя товару
                arr[item_name] = {
                    'Количество товара': item_qty,
                    'Средняя цена продажи': item_price,
                    'Общая сумма продажи': item_price * item_qty,  # Первоначальное значение - цена первой продажи
                    'Комиссия за продажу': commission_ratio * item_price
                }
            else:
                arr[item_name]['Количество товара'] += item_qty
                # Обновляем среднюю цену
                arr[item_name]['Средняя цена продажи'] = (
                    arr[item_name]['Средняя цена продажи'] * arr[item_name]['Количество товара'] + item_price * item_qty
                ) / (arr[item_name]['Количество товара'] + item_qty)
                # Обновляем общую сумму
                arr[item_name]['Общая сумма продажи'] = arr[item_name]['Количество товара'] * arr[item_name]['Средняя цена продажи']
                
            
        
    ostatok = get_data_ozon(client_id=client_id, api_key=api_key)
    end_arr = []
    profit = 0
    # Получение данных о комиссиях FBO
    fbo_commissions = {}

    for item in arr.keys():
        
        headers = {'Api-Key': str(api_key), 'Client-Id': str(client_id), 'Content-Type': 'application/json'}
        response = requests.post("https://api-seller.ozon.ru/" + 'v4/product/info/prices', headers=headers, json={
            "filter": {
                "offer_id": [item],
                "visibility": "ALL"
            },
            "limit": 100
        })
          # Raises an error for bad responses
        response.raise_for_status()  # Проверка успешности ответа
        res = response.json()  # Преобразование ответа в JSON
        

        
        if 'result' in res and 'items' in res['result'] and res['result']['items']:
            item_commissions = res['result']['items'][0]['commissions']
            fbo_deliv_to_customer_amount = item_commissions['fbo_deliv_to_customer_amount']
            fbo_return_flow_trans_max_amount = item_commissions['fbo_return_flow_trans_max_amount']
            fbo_commissions[item] = fbo_deliv_to_customer_amount + fbo_return_flow_trans_max_amount
            print(fbo_commissions[item])
        else:
            print('ОШИБКА!')

    for a in arr.keys():
        
        
        item_ostatok = ostatok.get(a, 'None')
        if item_ostatok != 'None' and isinstance(item_ostatok, (int, float)) and arr[a]['Количество товара'] != 0:
            turnover = item_ostatok / arr[a]['Количество товара']
        else:
            turnover = None

        # Добавление комиссии FBO к каждому товару
        fbo_commission_sum = fbo_commissions.get(a, 0)
        arr[a]['fbo_commission_sum'] = fbo_commission_sum

        profit += arr[a]['Общая сумма продажи'] - arr[a]['Комиссия за продажу'] - fbo_commission_sum
        end_arr.append({
            'Товар': a,
            'Средняя цена': arr[a]['Средняя цена продажи'],
            'Количество': arr[a]['Количество товара'],
            'Продано на': arr[a]['Общая сумма продажи'],
            'Сумма комиссий ОЗОН': arr[a]['Комиссия за продажу'] * arr[a]['Количество товара'],
            'Сумма комиссий ФБО': fbo_commission_sum * arr[a]['Количество товара'],
            'Прибыль с учетом комиссии ОЗОН и ФБО': arr[a]['Общая сумма продажи'] - arr[a]['Комиссия за продажу'] * arr[a]['Количество товара'] - fbo_commission_sum * arr[a]['Количество товара'],
            'Остаток': item_ostatok,
            'Оборачиваемость': round(turnover, 2) if turnover else None
        })

    df = pd.DataFrame(data=end_arr)
    if len(str(month)) < 2:
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "ozon",
                                f"ozon_0{month}_{year}.xlsx")
    else:
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "ozon",
                                f"ozon_{month}_{year}.xlsx")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    df.to_excel(report_path, index=False)
    print("Готово! Файл отчета с ОЗОН создан.")




def report_v2(month, year, config):
    cf = cfg(config)
    if not cf:
        return

    arr = dict()
    res = ozon(config, 'v2/finance/realization', {"month": month,
                                                  "year": year})
    with open('test.json', "w", encoding="utf-8") as file:
        json.dump(res, file, ensure_ascii=False, indent=4)
    

def get_full(date, config):
    res = ozon(config, 'v1/finance/realization', {"date": date})


def main():
    # report(api_key='2c7c749c-caa3-4f41-b06c-e0b0b7b51ab8' , client_id='469127' , month=8, year=2024)
    # report_v2(month=8, year=2024, config='sec_of_chameleon')
    pass


if __name__ == '__main__':
    main()
