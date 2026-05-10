"""Aiogram router registration."""

from aiogram import Dispatcher

from .menu import menu_router


def setup_routers(dp: Dispatcher) -> None:
    """Attach all module routers to the dispatcher."""
    dp.include_router(menu_router)
