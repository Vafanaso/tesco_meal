import asyncio
from aiogram import Dispatcher
from src.integrations.bot import bot
from src.keyboards.keyboards import general_menu_keyboard,products_keyboard
from src.handlers import setup_routers
from src.db.db import init_db

async def main():
    await init_db()

    dp = Dispatcher()
    setup_routers(dp)

    print("🚀 Bot is starting...")

    await dp.start_polling(bot)
    await general_menu_keyboard()


if __name__ == "__main__":
    asyncio.run(main())
