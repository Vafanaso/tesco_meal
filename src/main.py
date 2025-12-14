import asyncio
from aiogram import Dispatcher
from src.integrations.bot import bot
from src.handlers.handlers import register_handlers  # your handlers

async def main():
    dp = Dispatcher()
    register_handlers(dp)

    print("🚀 Bot is starting...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
