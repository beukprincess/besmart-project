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
    @user_router.message(Command("pay"))
    async def pay_cmd(message: types.Message):
        username = message.from_user.username
        if not username:
            username = message.from_user.first_name
        unique_code = f"user_{user_id}" 
        price_kopeks = 1000
        await db_client.add_user(message.from_user.id, username)
        text = (
        f"**Рахунок на оплату**\n"
        f"Сума: 1 грн\n\n"
        f"1. Перейдіть за посиланням: ---\n"
        f"2. Вкажіть суму **{price_kopeks/100} грн**\n"
        f"3. В коментарі до платежу ОБОВ'ЯЗКОВО вкажіть: `{unique_code}`\n\n"
        f"Після оплати натисніть кнопку 'Я оплатив'."
        )
    
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Я оплатив", callback_data=f"check_{unique_code}_{price_kopeks}")]
        ])
    
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")
