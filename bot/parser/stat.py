import datetime
from pprint import pprint

import psycopg2
import requests

from logs.loger import logger



import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))


# admins = [
#     '571104053',
#     '1629624048',
#     '176280312'
# ]

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



def db():
    # Параметры подключения к базе данных
    hostname = 'localhost'
    username = PGUSER
    password = PGPASSWORD
    database = DATABASE
    port = 5432

    # Установка соединения с базой данных
    conn = psycopg2.connect(
        host=hostname,
        user=username,
        password=password,
        dbname=database,
        port=port
    )

    # Создание курсора для выполнения SQL-запросов
    cur = conn.cursor()

    # cur.execute('SELECT * FROM "stat"')
    try:
        insert_query = "INSERT INTO stat (date, item_code, free_to_sell_amount) VALUES (%s, %s, %s)"

        resp_data = ozon()
        remainder = {}
        list_warehouse = resp_data['result']['rows']
        for n in list_warehouse:

            item_code = n['item_code']
            free_to_sell_amount = n['free_to_sell_amount']
            
            if item_code in remainder:
                remainder[item_code] += free_to_sell_amount
            else:
                remainder[item_code] = free_to_sell_amount
            
        

        date = datetime.datetime.now().strftime('%Y-%m-%d')
        remdate = {date: remainder}
        wrh = remdate
        items = wrh.items()
        for i in items:
            date = i[0]
            item = i[1]
            for n, r in item.items():
                data = (date, n, r)
                cur.execute(insert_query, data)
                conn.commit()
                # Закрытие курсора и соединения
        cur.close()
        conn.close()
        pprint('Done')
    except Exception as ex:
        logger.error(f'Обнаружена ошибка: {ex}')


def ozon():
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": aqua_client_id,
        "Api-Key": aqua_api_key,
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
    # with open('data/warehouses.json', 'w', encoding='utf-8') as file:
    #     json.dump(resp_data, file, ensure_ascii=False, indent=4)








def main():
    ozon()
    db()



if __name__ == '__main__':
    main()
