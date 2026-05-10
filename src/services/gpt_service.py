"""GPT-based steps: recipe generation, shopping list extraction, product picking."""

from asyncio import to_thread

from src.integrations.gpt import message_to_gpt


def get_recipe_from_gpt(budget: str, number_of_days: str) -> tuple[str, str]:
    """Ask GPT for a meal plan that fits a daily budget.

    The prompt tells GPT to put a comma-separated list of meal names on the
    first line, followed by full recipes. We split the first line off and
    return it as the short title.

    Args:
        budget: Tier label - "cheap" (~150 CZK/day), "normal" (~300),
            "snob" (500+).
        number_of_days: Plan length in days.

    Returns:
        Tuple of (short_meal_names_line, full_recipe_text).
    """
    prompt = (
        f"I want a {budget} recipe for {number_of_days} days. "
        f"Budget guidelines: cheap (~150 CZK/day), normal (~300 CZK/day), "
        f"snob (500+ CZK/day). "
        f"Format: The VERY FIRST line must be only the names of the meals "
        f"divided by commas. "
        f"Followed by the full recipe and description (max 3500 chars)."
    )

    recipe_content = message_to_gpt(prompt)
    first_line = recipe_content.strip().split("\n", 1)[0]
    name = first_line or "New Recipe"
    return name, recipe_content


def shopping_list(recipe: str) -> str:
    """Ask GPT to extract a comma-separated list of ingredients with prices.

    Args:
        recipe: The recipe text returned by ``get_recipe_from_gpt``.

    Returns:
        Raw GPT output, e.g. ``"Ovesné vločky 500 g – 29 Kč, Banán – 25 Kč"``.
    """
    return message_to_gpt(
        f"Give me a list of groceries for this recipe: {recipe}. "
        f"Return ONLY a comma-separated list of products and approximate prices in CZK. "
        f"Use readable Czech names with spaces (e.g. 'červená čočka', not 'červenáčočka'). "
        f"Example of a correct answer: "
        f"Ovesné vločky jemné 1 kg - 29 Kč, Banán - 29 Kč/kg, "
        f"Tesco Skořice mletá 40 g - 14 Kč"
    )


def get_shopping_list(recipe: str) -> list[str]:
    """Convert GPT's comma-separated ingredient string into a Python list.

    Args:
        recipe: Recipe text to derive ingredients from.

    Returns:
        List of "Name - price Kč" strings, one per ingredient.
    """
    raw = shopping_list(recipe)
    return [item.strip() for item in raw.split(",") if item.strip()]


def choosing_right_product(
    list_of_product_and_prices: list[tuple[str, float | str]], product: str
) -> str:
    """Pick the best SerpAPI hit for an ingredient, or estimate as a fallback.

    Args:
        list_of_product_and_prices: SerpAPI titles paired with prices. Empty
            list triggers the GPT estimate fallback.
        product: Original Czech ingredient name being searched for.

    Returns:
        A "Name, price" string. Falls back to a GPT estimate (with a
        " last resort GPT" suffix) if no SerpAPI hits were provided.
    """
    if list_of_product_and_prices:
        prompt = (
            f"Here is a list of products and prices: {list_of_product_and_prices}. "
            f"Choose the best option that fits the search '{product}'. "
            f"Answer strictly as a string with the name and price separated by a comma. "
            f"Use ONLY the name and price from the list I gave you. "
            f"Be careful: 'voda' (water) is not 'vodka'."
        )
        return message_to_gpt(prompt)

    prompt = (
        f"I want to buy {product} in a Tesco store in Prague, Czech Republic. "
        f"Tell me the approximate price. "
        f"Answer strictly as a string with the name and price separated by a comma. "
        f"Use the name I gave you, do not invent a different one."
    )
    return message_to_gpt(prompt) + " last resort GPT"


async def choosing_right_product_async(
    list_of_product_and_prices: list[tuple[str, float | str]], product: str
) -> str:
    """Async wrapper around ``choosing_right_product`` (runs blocking call in a thread)."""
    return await to_thread(choosing_right_product, list_of_product_and_prices, product)
