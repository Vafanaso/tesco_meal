"""Application entry point: initialise the database and start the Telegram bot."""

import asyncio

from aiogram import Dispatcher

from src.db.db import init_db
from src.handlers import setup_routers
from src.integrations.bot import bot


async def main() -> None:
    """Create tables, register routers, and start long-polling Telegram."""
    await init_db()

    dp = Dispatcher()
    setup_routers(dp)

    print("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
