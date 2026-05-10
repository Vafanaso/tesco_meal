"""Price extraction from free-form GPT/SerpAPI strings.

Both GPT and SerpAPI return product strings in inconsistent shapes:

    "Tesco Banana Chips 100g, 24.9"
    "Cibule - Tesco Groceries, 2,69 Kč"
    "Ovesné vločky jemné - 1 kg: 29 Kč"
    "Banán - 29 Kč/kg"
    "kariprášek, 25-35 Kč last resort GPT"

We need a single number to sum into a budget total. The strategy is:

1. Find every numeric token in the string.
2. Prefer one that is followed by 'Kč' (currency marker).
3. If a range like ``25-35 Kč`` appears, take the lower bound.
4. Fall back to the last number in the string if no Kč marker is present.
5. Return ``None`` for the price when we genuinely cannot find a number -
   the caller should treat that as "unpriced" rather than zero.
"""

from __future__ import annotations

import re

_PRICE_NEAR_KC = re.compile(
    r"(\d+(?:[.,]\d+)?)(?:\s*[-–]\s*\d+(?:[.,]\d+)?)?\s*Kč",
    re.IGNORECASE,
)
_ANY_NUMBER = re.compile(r"\d+(?:[.,]\d+)?")


def _to_float(token: str) -> float:
    """Convert ``"29,9"`` or ``"29.9"`` to ``29.9``."""
    return float(token.replace(",", "."))


def parse_price(raw: str) -> tuple[str, float | None]:
    """Split a raw product string into a clean name and a numeric price.

    Args:
        raw: Free-form product string from GPT or SerpAPI.

    Returns:
        Tuple of (name, price_in_czk). ``price_in_czk`` is ``None`` when no
        number could be extracted. The name is the part of ``raw`` before the
        matched price token, with trailing punctuation/separators stripped.

    Examples:
        >>> parse_price("Tesco Banana Chips 100g, 24.9")
        ('Tesco Banana Chips 100g', 24.9)
        >>> parse_price("Cibule - Tesco Groceries, 2,69 Kč")
        ('Cibule - Tesco Groceries', 2.69)
        >>> parse_price("kariprášek, 25-35 Kč last resort GPT")
        ('kariprášek', 25.0)
        >>> parse_price("just a name")
        ('just a name', None)
    """
    if not raw:
        return "", None

    text = raw.strip()

    match = _PRICE_NEAR_KC.search(text)
    if match:
        price = _to_float(match.group(1))
        name = text[: match.start()]
        return _clean_name(name) or text, price

    numbers = list(_ANY_NUMBER.finditer(text))
    if numbers:
        last = numbers[-1]
        price = _to_float(last.group(0))
        name = text[: last.start()]
        return _clean_name(name) or text, price

    return text, None


_TRAILING_JUNK = re.compile(r"[\s,;:\-–—]+$")


def _clean_name(name: str) -> str:
    """Strip whitespace and trailing separators left over after slicing the price out."""
    return _TRAILING_JUNK.sub("", name).strip()
