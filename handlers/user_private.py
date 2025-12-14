import asyncio
from aiogram import Router, F, types
from aiogram.types import FSInputFile, CallbackQuery
from services.logic import besmart_service, Result
from aiogram.filters import CommandStart
from keyboard.reply import get_main_kb, get_menu_kb
from aiogram.exceptions import TelegramBadRequest
from database.db import db_client
from states import Registration



user_router = Router()

@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    username = message.from_user.username
    if not username:
        username = message.from_user.first_name
    
    await db_client.add_user(message.from_user.id, username)
    print(f"User with id {message.from_user.id} was successfuly added.")
    await message.answer(
    "Вітаю тебе у курсах BeSmart!",
    reply_markup = get_main_kb()
    )
