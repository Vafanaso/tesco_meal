"""Telegram keyboards used by the menu flow."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from sqlalchemy import select

from src.db.db import SessionLocal
from src.db.models import Product


async def products_keyboard() -> InlineKeyboardMarkup:
    """Build the inline shopping-list keyboard from the current Product rows.

    Each row shows a green checkmark when ``Product.bought`` is true and an
    empty box otherwise. The product price is appended to the label when
    available so the user sees the cost on every button.

    Returns:
        Inline keyboard ready to attach to a Telegram message.
    """
    async with SessionLocal() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    buttons: list[list[InlineKeyboardButton]] = []
    for item in products:
        emoji = "✅" if item.bought else "⬜"
        price_part = f" - {item.price:g} Kč" if item.price is not None else ""
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{emoji} {item.name}{price_part}",
                    callback_data=f"product:{item.id}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def menu_type_keyboard() -> ReplyKeyboardMarkup:
    """Reply keyboard for choosing a budget tier."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Cheap"),
                KeyboardButton(text="Normal"),
                KeyboardButton(text="Snob"),
            ]
        ],
        resize_keyboard=True,
    )


def days_keyboard() -> ReplyKeyboardMarkup:
    """Reply keyboard for choosing how many days to plan for."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1"),
                KeyboardButton(text="2"),
                KeyboardButton(text="3"),
            ]
        ],
        resize_keyboard=True,
    )


def start_keyboard() -> ReplyKeyboardMarkup:
    """Persistent keyboard with a single 'Start' button to kick off the flow."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Start")]],
        resize_keyboard=True,
        input_field_placeholder="Press Start to begin",
    )
