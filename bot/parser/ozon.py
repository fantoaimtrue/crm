import json
import os
from calendar import monthrange
from pprint import pp, pprint

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



def report(date, config):
    cf = cfg(config)
    if not cf:
        return

    arr = dict()
    res = ozon(config, 'v1/finance/realization', {"date": date})
    if res.get('message'):
        print(res['message'])
        return

    for r in res['result']['rows']:
        if r['offer_id']:
            if r['offer_id'] not in arr:
                prices = [{'price': r['price'], 'qty': r['sale_qty']}]
                arr[r['offer_id']] = {
                    'qty': r['sale_qty'],
                    'sale_sum': r['sale_qty'] * r['price'],
                    'commission_sum': (r['sale_qty'] * r['price']) * r['commission_percent'] / 100,
                    'prices': prices,
                    'fbo_commission_sum': 0  # Инициализация поля для комиссии ФБО
                }
            else:
                arr[r['offer_id']]['qty'] += r['sale_qty']
                arr[r['offer_id']]['sale_sum'] += (r['sale_qty'] * r['price'])
                arr[r['offer_id']]['commission_sum'] += (r['sale_qty'] * r['price']) * r['commission_percent'] / 100
                arr[r['offer_id']]['prices'].append({'price': r['price'], 'qty': r['sale_qty']})

    for a in arr.values():
        total_price = sum(p['price'] * p['qty'] for p in a['prices'])
        total_qty = sum(p['qty'] for p in a['prices'])
        a['mid_price'] = round(total_price / total_qty, 2) if total_qty != 0 else 0

    ostatok = get_data_ozon(client_id=cf[1], api_key=cf[0])
    end_arr = []
    profit = 0

    current_year, month = map(int, date.split('-'))
    days = str(monthrange(current_year, month)[1])
    page = 1

    # Получение данных о комиссиях FBO
    fbo_commissions = {}

    for item in arr.keys():
        res = ozon(config, 'v4/product/info/prices', {
            "filter": {
                "offer_id": [item],
                "visibility": "ALL"
            },
            "limit": 100
        })

        if 'result' in res and 'items' in res['result'] and res['result']['items']:
            item_commissions = res['result']['items'][0]['commissions']
            fbo_deliv_to_customer_amount = item_commissions['fbo_deliv_to_customer_amount']
            fbo_return_flow_trans_max_amount = item_commissions['fbo_return_flow_trans_max_amount']
            fbo_commissions[item] = fbo_deliv_to_customer_amount + fbo_return_flow_trans_max_amount

    for a in arr.keys():
        item_ostatok = ostatok.get(a, 'None')
        if item_ostatok != 'None' and isinstance(item_ostatok, (int, float)) and arr[a]['qty'] != 0:
            turnover = item_ostatok / arr[a]['qty']
        else:
            turnover = None

        # Добавление комиссии FBO к каждому товару
        fbo_commission_sum = fbo_commissions.get(a, 0)
        arr[a]['fbo_commission_sum'] = fbo_commission_sum

        profit += arr[a]['sale_sum'] - arr[a]['commission_sum'] - fbo_commission_sum
        end_arr.append({
            'Товар': a,
            'Средняя цена': arr[a]['mid_price'],
            'Количество': arr[a]['qty'],
            'Продано на': arr[a]['sale_sum'],
            'Сумма комиссий ОЗОН': arr[a]['commission_sum'] * arr[a]['qty'],
            'Сумма комиссий ФБО': fbo_commission_sum * arr[a]['qty'],
            'Прибыль с учетом комиссии ОЗОН и ФБО': arr[a]['sale_sum'] - arr[a]['commission_sum'] * arr[a]['qty'] - fbo_commission_sum * arr[a]['qty'],
            'Остаток': item_ostatok,
            'Оборачиваемость': round(turnover, 2) if turnover else None
        })

    df = pd.DataFrame(data=end_arr)
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "ozon",
                               "aqua" if config == 'sec_of_chameleon' else "csc",
                               f"ozon_{config}_{date}.xlsx")
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
    pprint(res)


def main():
    report(date='2024-05', config='sec_of_chameleon')
    # report_v2(month=5, year=2024, config='sec_of_chameleon')


if __name__ == '__main__':
    main()
