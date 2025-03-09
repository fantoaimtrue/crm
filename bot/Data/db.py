import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

# db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

# Загружаем переменные окружения
load_dotenv()

# Получаем параметры подключения из переменных окружения
ip = str(os.getenv("IP"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
DB_PORT = os.getenv("DB_PORT")  # Добавьте получение порта из переменной окружения

DATABASE_URL = f"postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{ip}:{DB_PORT}/{DATABASE}"

# Создаем движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем фабрику сессий
async_session_factory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для получения новой сессии
def get_session() -> AsyncSession:
    return async_session_factory()


# Модель для таблицы профиля пользователя (аналогичная модели в Django)
class Profile(Base):
    __tablename__ = "userprofile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    email = Column(Text, nullable=True)
    tg_username = Column(Text, nullable=True)
    tg_first_name = Column(Text, nullable=True)
    tg_last_name = Column(Text, nullable=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True)


async def create_user(session: AsyncSession, user_data: dict):
    try:
        # Логика создания пользователя
        stmt = select(Profile).filter_by(telegram_id=user_data["telegram_id"])
        result = await session.execute(stmt)
        profile = result.scalars().first()

        if not profile:
            new_profile = Profile(
                telegram_id=user_data["telegram_id"],
                tg_username=user_data["username"],
                tg_first_name=user_data["first_name"],
                tg_last_name=user_data["last_name"],
            )
            session.add(new_profile)
            await session.commit()
            return True
        else:
            return False  # Пользователь уже существует
    except IntegrityError as e:
        await session.rollback()
        print(f"Ошибка при создании пользователя: {e}")
        return False
