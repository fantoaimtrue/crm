
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.set import BOT_TOKEN
from handlers import start  # Импортируем хэндлер для команды /start
from handlers import report  # Импортируем хэндлер для команды /start

# from db import create_tables, create_db_pool


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# async def on_startup(dispatcher: Dispatcher):
    # await create_tables()  # Создание таблицы при запуске бота
    # start.db_pool = await create_db_pool()

    # await bot.send_message(chat_id=settings.ADMIN_ID, text="Bot is up and running!")


def main():
    dp.include_router(start.router)
    dp.include_router(report.router)

    # dp.startup.register(on_startup)

    dp.run_polling(bot)


if __name__ == '__main__':
    main()
