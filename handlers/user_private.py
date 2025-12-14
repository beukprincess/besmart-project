import asyncio
from aiogram import Router, F, types
from aiogram.types import FSInputFile, CallbackQuery
from services.logic import besmart_service, Result
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboard.reply import get_main_kb, get_menu_kb
from aiogram.exceptions import TelegramBadRequest
from database.db import db_client
from states import Registration


user_router = Router()

@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    courses = await db_client.get_courses()
    builder = InlineKeyboardBuilder()
    for course in courses:
        # course = (id, name, price, schedule)
        builder.button(text=f"{course[1]}", callback_data=f"view_course:{course[0]}")
    builder.adjust(1)
    
    await message.answer("Привіт! Обери курс для навчання:", reply_markup=builder.as_markup())

@user_router.callback_query(F.data.startswith("view_course:"))
async def view_course(callback: types.CallbackQuery, state: FSMContext):
    course_id = int(callback.data.split(":")[1])
    course = await db_client.get_course_by_id(course_id)
    
    await state.update_data(course_id=course_id, schedule=course[3])
    
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатити {course[2]} грн", callback_data="pay_confirm")
    builder.button(text="Назад", callback_data="back_to_menu")
    
    await callback.message.edit_text(
        f"Курс: <b>{course[1]}</b>\nЦіна: {course[2]} грн\nРозклад: {course[3]}",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
