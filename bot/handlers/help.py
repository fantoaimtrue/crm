from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    await message.answer("This is the help message. Here you can find information on how to use the bot.")
