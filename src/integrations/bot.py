"""Single shared aiogram Bot instance, configured from ``.env``."""

from aiogram import Bot

from src.config.settings import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
