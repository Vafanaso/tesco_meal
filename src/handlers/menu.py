from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup # Added missing imports
from src.keyboards.keyboards import (
    general_menu_keyboard,
    products_keyboard,
    menu_type_keyboard,
    days_keyboard
)
from src.services.full_product_search import seed, full_search_async_serp, full_search_async_gpt
from src.db.models import Product
from src.db.db import SessionLocal

menu_router = Router()

class MenuStates(StatesGroup):
    choosing_type = State()
    choosing_days = State()
    processing = State()
    products_listing = State()

@menu_router.message(CommandStart()) # Correct filter usage
@menu_router.message(F.text == "Start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MenuStates.choosing_type)
    await message.answer(
        "👋 Welcome! Choose your menu type:",
        reply_markup=menu_type_keyboard()
    )

@menu_router.message(MenuStates.choosing_type, F.text.in_(["Budget", "Normal", "Snob"]))
async def choose_type(message: Message, state: FSMContext):
    await state.update_data(menu_type=message.text.lower())
    await state.set_state(MenuStates.choosing_days)
    await message.answer(
        f"Selected: {message.text}. Now choose for how many days:",
        reply_markup=days_keyboard()
    )


@menu_router.message(MenuStates.choosing_days, F.text.in_(["1", "2", "3"]))
async def choose_days(message: Message, state: FSMContext):
    user_data = await state.get_data()
    menu_type = user_data.get('menu_type')
    num_days = message.text

    await state.set_state(MenuStates.processing)
    await message.answer(
        f"⏳ Generating {menu_type} menu for {num_days} days...",
        reply_markup=ReplyKeyboardRemove()
    )

    # Unpack the recipe text and the result list
    # recipe_text, result_list = await full_search_async_serp(menu_type, num_days)
    recipe_text, result_list = await full_search_async_gpt(menu_type, num_days)


    # 1. Send the Menu/Recipe text first
    await message.answer(f"📋 **Your Menu:**\n\n{recipe_text}", parse_mode="Markdown")

    # 2. Seed the database with the products
    await seed(result_list)

    # 3. Send the interactive shopping list keyboard
    kb = await products_keyboard()
    await message.answer("🛒 **Your Shopping List:**", reply_markup=kb)
    await state.set_state(MenuStates.products_listing)

@menu_router.callback_query(F.data.startswith("product:"))
async def toggle_product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])

    async with SessionLocal() as session:
        product = await session.get(Product, product_id)
        if product:
            product.bought = not product.bought
            await session.commit()

    kb = await products_keyboard()
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()