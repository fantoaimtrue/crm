from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.future import select
from Data.models import Profile
from Data.db import get_session
   

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    session = get_session()
    try:
        # Выполнение запроса к базе данных
        tg_user = f'@{message.from_user.username}'
        result = await session.execute(select(Profile).where(Profile.tg_username == tg_user))
        profile = result.scalars().first()

        if profile:
            await message.answer(f"Ваш email: {profile.email}")
        else:
            await message.answer("Профиль не найден.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await session.close()
