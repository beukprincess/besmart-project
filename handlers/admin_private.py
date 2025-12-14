import asyncio
from aiogram import Router, types
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from database.db import db_client
from config import config
from states import AdminStates

admin_router = Router()


admin_router.message.filter(lambda message: message.from_user.id in config.admin_ids)

@admin_router.message(Command("sendall"))
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer("msg(text, photo, vid):")

    await state.set_state(AdminStates.wait_for_broadcast_content)

@admin_router.message(AdminStates.wait_for_broadcast_content)
async def process_broadcast(message: types.Message, state: FSMContext):
    users = await db_client.get_all_users()
    
    await message.answer(f"Started. Users - {len(users)} ...")
    
    sent_count = 0
    blocked_count = 0

    for user_id in users:
        try:
            await message.copy_to(chat_id=user_id)
            sent_count += 1
            
        except TelegramForbiddenError:
            blocked_count += 1
        except Exception as e:
            print(f"Помилка з {user_id}: {e}")

        await asyncio.sleep(0.05) 

    await message.answer(
        f"Отримали: {sent_count}\n"
        f"Заблокували бота: {blocked_count}"
    )
    
    await state.clear()