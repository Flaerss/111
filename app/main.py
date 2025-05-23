import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv
from app.handlers import client_handlers
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

async def main():
    try:
        # Проверка обязательных переменных
        if not os.getenv("BOT_TOKEN"):
            raise ValueError("Переменная окружения BOT_TOKEN не задана")

        # Инициализация бота
        bot = Bot(
            token=os.getenv("BOT_TOKEN"),
            parse_mode=ParseMode.HTML
        )
        dp = Dispatcher()
        dp.include_router(client_handlers.router)

        # Запуск бота
        logging.info("Запуск бота...")
        async with bot.context():
            await dp.start_polling(bot)
            logging.info("Бот успешно запущен")

    except TokenValidationError:
        logging.error("⚠️ Неверный токен бота!")
        print("⚠️ Неверный токен бота!")

    except Exception as e:
        logging.error(f"🚨 Критическая ошибка: {e}")
        print(f"🚨 Критическая ошибка: {e}")

    finally:
        logging.info("Завершение работы бота...")

if __name__ == "__main__":
    asyncio.run(main())
