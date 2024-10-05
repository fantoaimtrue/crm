import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.set import BOT_TOKEN
from handlers import start, report
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from Data.db import init_db, get_session
from decouple import config, Csv





bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# async def on_startup(dispatcher: Dispatcher):
#     await init_db()  # Инициализация базы данных
#     start.db_session = get_session()  # Передаем сессию в хэндлеры
#     report.db_session = get_session()  # То же самое для других хэндлеров

def main():
    dp.include_router(start.router)
    dp.include_router(report.router)

    # dp.startup.register(on_startup)

    dp.run_polling(bot)

if __name__ == '__main__':
    main()
