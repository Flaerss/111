import os
from aiogram import Bot
from db import log_message

bot = Bot(token=os.getenv("BOT_TOKEN"))

async def send_notification(event_type, name, date):
    text = ""
    if event_type == "new":
        text = f"{name}, вы записаны на {date}"
    elif event_type == "rescheduled":
        text = f"{name}, ваша запись перенесена на {date}"
    elif event_type == "cancelled":
        text = f"{name}, ваша запись отменена."

    await bot.send_message(chat_id=os.getenv("OWNER_ID"), text=text)
    log_message(name, f"[Автоуведомление]: {text}")