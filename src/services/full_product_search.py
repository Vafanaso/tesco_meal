"""Top-level search orchestration: combines GPT recipe + shopping list + per-item lookup."""

import asyncio
from asyncio import to_thread

from sqlalchemy import delete

from src.db.db import SessionLocal
from src.db.models import Product
from src.services.gpt_service import (
    choosing_right_product_async,
    get_recipe_from_gpt,
    get_shopping_list,
)
from src.services.serp_service import get_price_async
from src.utils.price import parse_price


async def process_product(product: str) -> str:
    """Look up SerpAPI prices for one ingredient and ask GPT to pick the best one.

    Args:
        product: Czech ingredient name (e.g. "rýže").

    Returns:
        A "Name, price" string chosen by GPT from SerpAPI hits, or a GPT
        fallback estimate if SerpAPI returned nothing.
    """
    prod_options = await get_price_async(product)
    best_pick = await choosing_right_product_async(prod_options, product)
    return best_pick


async def full_search_async_serp(
    budget: str, number_of_days: str
) -> tuple[str, list[str]]:
    """Generate a recipe and resolve every ingredient via SerpAPI + GPT.

    Args:
        budget: One of "cheap", "normal", "snob" (price tier).
        number_of_days: How many days the meal plan should cover.

    Returns:
        Tuple of (recipe_text, list_of_resolved_product_strings).
    """
    _, recipe = get_recipe_from_gpt(budget, number_of_days)
    full_shop_list = await to_thread(get_shopping_list, recipe)

    tasks = [process_product(item) for item in full_shop_list]
    results = await asyncio.gather(*tasks)
    return recipe, list(results)


async def full_search_async_gpt(
    budget: str, number_of_days: str
) -> tuple[str, list[str]]:
    """Generate a recipe and ask GPT (only) to produce a priced shopping list.

    Used when SerpAPI quota is exhausted. Cheaper but prices are estimates.

    Args:
        budget: One of "cheap", "normal", "snob" (price tier).
        number_of_days: How many days the meal plan should cover.

    Returns:
        Tuple of (recipe_text, list_of_product_strings_with_prices).
    """
    _, recipe = get_recipe_from_gpt(budget, number_of_days)
    full_shop_list = await to_thread(get_shopping_list, recipe)
    return recipe, full_shop_list


async def seed(products: list[str]) -> None:
    """Replace the Product table with the given items.

    Each input string is parsed into (name, price) before insert. The previous
    shopping list is wiped so each new menu starts from a clean slate.

    Args:
        products: Strings like "Tesco Oats 500g, 29.9 Kč".
    """
    async with SessionLocal() as session:
        await session.execute(delete(Product))
        for item in products:
            name, price = parse_price(item)
            session.add(Product(name=name, price=price))
        await session.commit()
