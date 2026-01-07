from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.keyboards.keyboards import general_menu_keyboard, products_keyboard
from src.services.full_product_search import full_search_async, seed
from src.db.models import Product
from src.db.db import SessionLocal

menu_router = Router()


class MenuStates(StatesGroup):
    start = State()
    choosing_budget = State()
    products_listing = State()


@menu_router.message(F.text == "Start" or F.text == CommandStart)
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuStates.start)
    await message.answer(
        "👋 AHOJ! Use buttons below",
        reply_markup=general_menu_keyboard(),
    )


@menu_router.message(StateFilter(MenuStates.start), F.text.isdigit())
async def money(money: Message, state: FSMContext):
    await state.set_state(MenuStates.choosing_budget)
    processing = await money.answer("⏳ Processing...")
    result_list = await full_search_async(money.text)
    await seed(result_list)
    kb = await products_keyboard()
    await money.answer("your list", reply_markup=kb)
    # result = "\n".join(result_list)
    # await processing.delete()
    # await money.answer(result)


@menu_router.callback_query(F.data.startswith("product:"))
async def toggle_product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])

    async with SessionLocal() as session:
        product = await session.get(Product, product_id)
        product.bought = not product.bought
        await session.commit()

    kb = await products_keyboard()
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

#TODO add proccesing to ignore