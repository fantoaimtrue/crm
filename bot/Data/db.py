import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Загружаем переменные окружения
load_dotenv()

# Получаем параметры подключения из переменных окружения
ip = os.getenv('IP')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))
DATABASE_URL = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'

# Создаем движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем фабрику сессий
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для получения новой сессии
def get_session() -> AsyncSession:
    return async_session_factory()
