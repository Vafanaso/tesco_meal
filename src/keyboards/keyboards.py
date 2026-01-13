from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from src.db.db import SessionLocal
from src.db.models import Product
from sqlalchemy import select


async def products_keyboard():
    async with SessionLocal() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    buttons = []
    for item in products:
        emoji = "✅" if item.bought else "⬜"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{emoji} {item.name}", callback_data=f"product:{item.id}"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def general_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Start"),
                KeyboardButton(text="New menu"),
            ],
            [
                KeyboardButton(text="Menu"),
                KeyboardButton(text="List of products"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose an action…",
    )
