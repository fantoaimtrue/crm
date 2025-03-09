from math import log
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import webapp
from logger_config import logger

router = Router()


@router.message(Command(commands=["crm"]))
async def open_webapp(message: Message):
    
    try:
        # Отправляем сообщение с кнопкой
        await message.answer(
            "Нажмите на кнопку ниже, чтобы открыть Web-панель:",
            reply_markup=webapp()
        )
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}", exc_info=True)