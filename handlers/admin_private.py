import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from database.db import db_client
from config import config
from states import AdminStates
import os
import pandas as pd

admin_router = Router()


admin_router.message.filter(lambda message: message.from_user.id in config.admin_ids)

@admin_router.message(Command("sendall"))
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer("msg(text, photo, vid):")

    await state.set_state(AdminStates.wait_for_broadcast_content)

@admin_router.message(AdminStates.wait_for_broadcast_content)
async def process_broadcast(message: types.Message, state: FSMContext):
    users = await db_client.get_all_students()
    
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

@admin_router.message(F.document)
async def process_attendance_file(message: types.Message):
    if not message.document.file_name.endswith('.xlsx'):
        await message.answer("Це не Excel файл (.xlsx)")
        return

    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = f"attendance_{message.document.file_name}"
    
    await message.bot.download_file(file.file_path, file_path)
    
    try:
        df = pd.read_excel(file_path)
        
        required_cols = ['user_id', 'attendance']
        if not all(col in df.columns for col in required_cols):
            await message.answer("У файлі немає колонок 'user_id' або 'attendance'")
            return
            
        count_sent = 0
        
        for index, row in df.iterrows():
            status = str(row['attendance']).strip().upper()
            user_id = row['user_id']
            
            if status in ['Н', 'H']: 
                try:
                    await message.bot.send_message(
                        chat_id=user_id,
                        text="Ви були відсутні на сьогоднішньому занятті."
                    )
                    count_sent += 1
                except Exception as e:
                    print(f"Не вдалося надіслати юзеру {user_id}: {e}")

        await message.answer(f"Обробка завершена. Сповіщень про відсутність: {count_sent}")

    except Exception as e:
        await message.answer(f"Помилка обробки файлу: {e}")
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)