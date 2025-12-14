# import sys
# import asyncio
# import logging
# from aiogram import Bot, Dispatcher, html
# from aiogram.enums import ParseMode
# from aiogram.client.default import DefaultBotProperties
#
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from src.config.settings import BOT_TOKEN
#
# dp = Dispatcher()
# TOKEN = BOT_TOKEN
#
#
# @dp.message(CommandStart())
# async def start_command(message: Message):
#     await message.answer("Oi, i can give you THE menu bruv")
# # @dp.message()
# # async def gpt_answer_handler(message: Message) -> None:
# #     prompt:str = f"I would like to create a menu for {message.text} krouns, i will buy everything in tesco in prague, just give a list of products and aproximate prices and total price and nothing else, no text before and no text after"
# #     await message.answer(mes(prompt))
