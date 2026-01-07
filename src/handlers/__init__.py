from .menu import menu_router


def setup_routers(dp):
    dp.include_router(menu_router)
