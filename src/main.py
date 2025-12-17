import asyncio
from aiogram import Dispatcher
from src.integrations.bot import bot
from src.keyboards.keyboards import general_menu_keyboard
from src.handlers import setup_routers

async def main():
    dp = Dispatcher()
    setup_routers(dp)

    print("🚀 Bot is starting...")

    await dp.start_polling(bot)
    await general_menu_keyboard()


if __name__ == "__main__":
    asyncio.run(main())
