import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import db_client
from config import config
from handlers.user_private import user_router
from handlers.admin_private import admin_router

if not config.token:
    print("Token was not found")
else:
    print("Token was found successfuly")

async def on_startup():
    await db_client.create_table()
    print("Database connected;")

async def main():
    bot = Bot(token=config.token)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot disabled.")