from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
# from db import create_user
from keyboards.default import kb_report

router = Router()

# Инициализация подключения к БД
# db_pool = None

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    # await create_user(
    #     message.from_user.id,
    #     message.from_user.username,
    #     message.from_user.first_name,
    #     message.from_user.last_name
    # )
    await message.answer("Для получения отчета введите /report")
