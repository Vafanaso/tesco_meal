"""SerpAPI-based price lookup for individual products."""

from asyncio import to_thread

from src.exceptions.exceptions import InvalidSearchResult
from src.integrations.serp_api import serp_search
from src.prompts import snippet_price_search
from src.schemas.serp import SerpResults


def get_price(product: str) -> list[tuple[str, str | float]]:
    """Look up Tesco prices for a product via SerpAPI Google search.

    Walks the organic results, preferring the structured rich-snippet price.
    Falls back to asking GPT to extract a price from the snippet text. Stops
    once three usable hits are collected.

    Args:
        product: Generic Czech ingredient name (e.g. "rýže").

    Returns:
        Up to three (title, price) pairs from SerpAPI. The price may be a
        ``float`` (from rich snippet) or a ``str`` like ``"29.9 Kč"`` (from
        the GPT snippet extractor). Empty list if nothing usable was found.

    Raises:
        InvalidSearchResult: If SerpAPI returned no ``organic_results`` field.
    """
    prices: list[tuple[str, str | float]] = []
    results: SerpResults = serp_search(product)

    try:
        max_products_amount = len(results.organic_results)
    except KeyError as e:
        raise InvalidSearchResult("Invalid product name for Serp API") from e

    i = 0
    while len(prices) < 3 and i < max_products_amount:
        item = results.organic_results[i]
        title: str = item.title

        if (
            item.rich_snippet
            and item.rich_snippet.bottom
            and item.rich_snippet.bottom.detected_extensions
            and item.rich_snippet.bottom.detected_extensions.price is not None
        ):
            price: str | float = item.rich_snippet.bottom.detected_extensions.price
        else:
            snippet = item.snippet or ""
            price = snippet_price_search(product, snippet)
            if price in ("GPT + SERP: no price", "GPT + SERP: no price."):
                i += 1
                continue

        prices.append((title, price))
        i += 1

    return prices


async def get_price_async(product: str) -> list[tuple[str, str | float]]:
    """Async wrapper around ``get_price`` (runs blocking SerpAPI call in a thread)."""
    return await to_thread(get_price, product)
