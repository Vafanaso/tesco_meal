"""Telegram handlers for the budget meal-planning flow."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy import select

from src.db.db import SessionLocal
from src.db.models import Product
from src.keyboards.keyboards import (
    days_keyboard,
    menu_type_keyboard,
    products_keyboard,
    start_keyboard,
)
from src.services.full_product_search import (
    full_search_async_gpt,
    full_search_async_serp,
    seed,
)

menu_router = Router()


class MenuStates(StatesGroup):
    """FSM states for the menu-creation flow."""

    choosing_type = State()
    choosing_days = State()
    processing = State()
    products_listing = State()


@menu_router.message(CommandStart())
@menu_router.message(F.text == "Start")
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Reset state and ask the user to pick a budget tier."""
    await state.clear()
    await state.set_state(MenuStates.choosing_type)
    await message.answer(
        "Welcome! Choose your menu type:",
        reply_markup=menu_type_keyboard(),
    )


@menu_router.message(
    MenuStates.choosing_type, F.text.in_(["Cheap", "Normal", "Snob"])
)
async def choose_type(message: Message, state: FSMContext) -> None:
    """Store the chosen budget tier and ask how many days to plan."""
    await state.update_data(menu_type=message.text.lower())
    await state.set_state(MenuStates.choosing_days)
    await message.answer(
        f"Selected: {message.text}. Now choose how many days:",
        reply_markup=days_keyboard(),
    )


@menu_router.message(MenuStates.choosing_days, F.text.in_(["1", "2", "3"]))
async def choose_days(message: Message, state: FSMContext) -> None:
    """Run the GPT search, persist the shopping list, and reply with totals."""
    user_data = await state.get_data()
    menu_type = user_data.get("menu_type", "normal")
    num_days = message.text or "1"

    await state.set_state(MenuStates.processing)
    await message.answer(
        f"Generating {menu_type} menu for {num_days} days...",
        reply_markup=ReplyKeyboardRemove(),
    )

    #recipe_text, result_list = await full_search_async_gpt(menu_type, num_days)
    recipe_text, result_list = await full_search_async_serp(menu_type, num_days)

    await message.answer(f"Your menu:\n\n{recipe_text}")

    await seed(result_list)

    total = await _shopping_list_total()
    kb = await products_keyboard()
    await message.answer(
        f"Your shopping list (estimated total: {total:g} Kč):",
        reply_markup=kb,
    )
    await message.answer("When you're done, press Start for a new menu.", reply_markup=start_keyboard())
    await state.set_state(MenuStates.products_listing)


@menu_router.callback_query(F.data.startswith("product:"))
async def toggle_product(callback: CallbackQuery) -> None:
    """Toggle the ``bought`` flag on a product when its button is tapped."""
    if not callback.data:
        return
    product_id = int(callback.data.split(":")[1])

    async with SessionLocal() as session:
        product = await session.get(Product, product_id)
        if product:
            product.bought = not product.bought
            await session.commit()

    kb = await products_keyboard()
    if callback.message:
        await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


async def _shopping_list_total() -> float:
    """Sum the ``price`` column across all products currently in the table.

    Returns:
        Total in CZK; products with ``price IS NULL`` are skipped.
    """
    async with SessionLocal() as session:
        result = await session.execute(select(Product.price))
        return sum(p for (p,) in result.all() if p is not None)
