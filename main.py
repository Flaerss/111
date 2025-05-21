from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from webhook import routes
from db import init_db, add_client, log_message, get_auto_reply, set_auto_reply
import logging
import asyncio
from aiohttp import web
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать в Фотостудию SVET Златоуст!")

@dp.message_handler(commands=["автоответ"])
async def change_auto_reply(message: types.Message):
    parts = message.text.split(" ", 1)
    if len(parts) == 1:
        reply = get_auto_reply()
        await message.answer(f"Текущий автоответ:

{reply}")
    else:
        set_auto_reply(parts[1])
        await message.answer("Автоответ обновлён.")

@dp.message_handler()
async def handle_any_message(message: types.Message):
    if message.text.startswith("/"):
        return
    reply = get_auto_reply()
    await message.answer(reply)
    add_client(message.from_user.full_name)
    log_message(message.from_user.full_name, f"[Клиент написал]: {message.text}")

def start_bot_and_webhook():
    loop = asyncio.get_event_loop()
    app = web.Application()
    app.add_routes(routes)
    loop.create_task(dp.start_polling())
    web.run_app(app, port=8080)

if __name__ == "__main__":
    init_db()
    start_bot_and_webhook()