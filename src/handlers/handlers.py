from curses.ascii import isdigit

from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import CommandStart,  StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.integrations.gpt import message_to_gpt
from src.keyboards.keyboards import general_menu_keyboard

router = Router()

class Form(StatesGroup):
    start = State()
    price = State()
    list = State()

@router.message(CommandStart())
@router.message(F.text == 'Start')

async def start(message:Message, state: FSMContext) -> None:
    await state.set_state(Form.start)
    await message.answer(
        "👋 AHOJ! Use buttons below",
        reply_markup=general_menu_keyboard(),
    )

def register_handlers(dp):
    dp.include_router(router)

@router.message(StateFilter(Form.start), F.text.isdigit())
async def money(money:Message, state: FSMContext):
    await money.answer(message_to_gpt(f'give me a menu for {money.text} czk, and tell me what to buy'))

