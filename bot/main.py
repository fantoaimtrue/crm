import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from aiogram.types import BotCommand
from config.set import BOT_TOKEN
from handlers import start, report, webapp
from Data.db import init_db, get_session
from decouple import config

WEBHOOK_HOST = config("WEBHOOK_HOST", default="https://crmmarketplacehelper.ru")  # URL хоста
WEBHOOK_PATH = "/webhook/"  # Путь для вебхука
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def on_startup(dispatcher: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)  # Устанавливаем вебхук
    # await init_db()  # Инициализация базы данных
    # start.db_session = get_session()  # Передаем сессию в хэндлеры
    # report.db_session = get_session()  # То же самое для других хэндлеров

async def on_shutdown(dispatcher: Dispatcher):
    await bot.delete_webhook()  # Удаляем вебхук при завершении

def main():
    dp.include_router(start.router)
    dp.include_router(report.router)
    # dp.include_router(webapp.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)


    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    web.run_app(app, host="0.0.0.0", port=8443)  # Меняйте порт при необходимости

if __name__ == '__main__':
    main()
