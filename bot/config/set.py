import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))


admins = [
    571104053,
    1629624048,
    176280312,
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
