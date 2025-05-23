from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import Config
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Синхронная версия для миграций и административных задач
sync_engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
)

# Асинхронная версия для работы бота
async_engine = create_async_engine(
    Config.SQLALCHEMY_DATABASE_URI.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=False,
    future=True
)

# Сессии
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

def init_db():
    """Инициализация таблиц в базе данных"""
    Base.metadata.create_all(bind=sync_engine)
    logging.info("Таблицы базы данных инициализированы")

async def get_async_db():
    """Асинхронный генератор сессий для бота"""
    async with AsyncSessionLocal() as session:
        yield session

def get_sync_db():
    """Синхронный генератор сессий для веб-интерфейса"""
    with SyncSessionLocal() as session:
        yield session

# Пример использования
async def example_usage():
    async with get_async_db() as db:
        # Ваш код работы с базой данных
        pass

if __name__ == "__main__":
    try:
        init_db()  # Инициализация базы данных при запуске
        example_usage()  # Пример асинхронного использования
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}")
