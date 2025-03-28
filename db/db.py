from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

DB_LOGIN = os.getenv("DB_LOGIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST= os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size = 5,
    max_overflow = 10,) 

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Функция для получения сессии
async def get_db():
    async with SessionLocal() as session:
        yield session

# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаём таблицу, если нет