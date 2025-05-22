import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from handlers import register_handlers
from scheduler import start_scheduler

# Загрузка переменных окружения из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Регистрация обработчиков
register_handlers(dp)

# Запуск
if __name__ == "__main__":
    start_scheduler(dp, bot)
    executor.start_polling(dp, skip_updates=True)
