"""Tiny prompt helpers used by the SerpAPI flow."""

from src.integrations.gpt import message_to_gpt


def snippet_price_search(product: str, snippet: str) -> str:
    """Ask GPT to extract a price from a SerpAPI snippet for a given product.

    Args:
        product: The product the snippet is supposed to be about.
        snippet: Raw text snippet from a SerpAPI organic result.

    Returns:
        A "<number> Kč" string, or the literal "GPT + SERP: no price"
        when no price could be extracted.
    """
    return message_to_gpt(
        f"I am sending you a snippet regarding {product}. "
        f"Find a price and send ONLY numbers + Kč. "
        f"If no price, return exactly: GPT + SERP: no price. "
        f"Snippet: {snippet}"
    )
