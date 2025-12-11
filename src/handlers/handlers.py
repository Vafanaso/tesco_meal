from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from src.integrations.gpt import message_to_gpt

router = Router()

@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Oi, ima give u a menu bruv")

def register_handlers(dp):
    dp.include_router(router)

@router.message()
async def money(money:Message):
    await money.answer(message_to_gpt(f'give me a menu for {money.text} krouns, ans tll me what to buy'))
