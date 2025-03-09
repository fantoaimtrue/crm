# main.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import instruction
from decouple import config, Csv
import time
import hashlib
import hmac
import requests
from Data.db import create_user, get_session  # Получаем сессию для работы с БД

router = Router()



@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer('Для дальнейшей работы, ознакомьтесь с инструкцией и напишите /report', reply_markup=instruction())
    
