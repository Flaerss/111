from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from app.services.yclients_service import YClientsAPI  # Исправленный импорт
from app.database import get_async_db

router = Router()
yc = YClientsAPI()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    async with get_async_db() as db:
        # Ваша логика обработки команды /start
        await message.answer(
            "Добро пожаловать!",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(Command("booking"))
async def booking_handler(message: types.Message):
    await message.answer("Введите дату в формате ДД.ММ.ГГГГ ЧЧ:ММ")
