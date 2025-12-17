from aiogram import Router, F
from asyncio import to_thread

from aiogram.types import Message
from aiogram.filters import CommandStart,  StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.keyboards.keyboards import general_menu_keyboard
from src.integrations.gpt import message_to_gpt
from src.services.full_product_search import  full_search_async

menu_router = Router()

class MenuStates(StatesGroup):
    start = State()
    choosing_budget = State()
    products_listing = State()

@menu_router.message(F.text == 'Start' or F.text == CommandStart)

async def start(message:Message, state: FSMContext) -> None:
    await state.set_state(MenuStates.start)
    await message.answer(
        "👋 AHOJ! Use buttons below",
        reply_markup=general_menu_keyboard(),
    )


@menu_router.message(StateFilter(MenuStates.start), F.text.isdigit())
async def money(money:Message, state: FSMContext):
    await state.set_state(MenuStates.choosing_budget)
    processing = await money.answer("⏳ Processing...")
    result_list =  await full_search_async(money.text)
    result = "\n".join(result_list)
    await processing.delete()
    await money.answer(result)
