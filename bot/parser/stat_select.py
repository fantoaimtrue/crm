import os
import datetime
from pprint import pprint
import psycopg2
import requests
import pandas as pd
from datetime import date

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))


admins = [
    '571104053',
    # '1629624048',
    # '176280312'
]

ip = os.getenv('IP')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))


csc_api_key = str(os.getenv('CSC_API_KEY'))
csc_client_id = str(os.getenv('CSC_CLIENT_ID'))

aqua_api_key = str(os.getenv('AQUA_API_KEY'))
aqua_client_id = str(os.getenv('AQUA_CLIENT_ID'))

wb_aqua_api_key = str(os.getenv('WB_AQUA_API_KEY'))


POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'



def ozon(api, id):
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": id,
        "Api-Key": api,
        "Content-Type": "application/json"
    }

    get_url = "https://api-seller.ozon.ru/v2/analytics/stock_on_warehouses"

    json_data = {
        "limit": 1000,
        "offset": 0,
        "warehouse_type": "ALL"
    }

    # Получение информации об отчёте
    resp_data = requests.post(get_url, headers=headers, json=json_data).json()

    return resp_data



def db(api, id):
    resp_data = ozon(api, id)
    remainder = {}
    end_rem = []
    list_warehouse = resp_data['result']['rows']
    for n in list_warehouse:

        item_code = n['item_code']
        free_to_sell_amount = n['free_to_sell_amount']
        
        if item_code in remainder:
            remainder[item_code] += free_to_sell_amount
        else:
            remainder[item_code] = free_to_sell_amount
    end_rem.append(remainder)
    df = pd.DataFrame(list(remainder.items()), columns=['Наименование', 'Количество'])
    df.to_excel(
                    os.path.dirname(os.path.abspath(__file__)) + "/reports/remains/aqua/aqua_" + ".xlsx",
                    index=False)

    return remainder
    

def main():
    ozon(api=csc_api_key, id=csc_api_key)
    db(api=csc_api_key, id=csc_client_id)



if __name__ == '__main__':
    main()


