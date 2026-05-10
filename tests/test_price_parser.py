"""Tests for the GPT/SerpAPI price-extraction helper."""

import pytest

from src.utils.price import parse_price


@pytest.mark.parametrize(
    "raw, expected_name, expected_price",
    [
        ("Tesco Banana Chips 100g, 24.9", "Tesco Banana Chips 100g", 24.9),
        ("Cibule - Tesco Groceries, 2,69 Kč", "Cibule - Tesco Groceries", 2.69),
        (
            "Vitana Pepř černý mletý 18g - Tesco Groceries, 21.9 Kč",
            "Vitana Pepř černý mletý 18g - Tesco Groceries",
            21.9,
        ),
        (
            "Ovesné vločky jemné - 1 kg: 29 Kč",
            "Ovesné vločky jemné - 1 kg",
            29.0,
        ),
        ("Banán - 29 Kč/kg", "Banán", 29.0),
        ("kariprášek, 25-35 Kč last resort GPT", "kariprášek", 25.0),
        ("Tesco Sliced Bread 500g,37.9", "Tesco Sliced Bread 500g", 37.9),
    ],
)
def test_parse_price_extracts_number_and_name(
    raw: str, expected_name: str, expected_price: float
) -> None:
    name, price = parse_price(raw)
    assert name == expected_name
    assert price == pytest.approx(expected_price)


def test_parse_price_returns_none_when_no_number() -> None:
    name, price = parse_price("just a name")
    assert name == "just a name"
    assert price is None


def test_parse_price_handles_empty_input() -> None:
    name, price = parse_price("")
    assert name == ""
    assert price is None


def test_parse_price_prefers_kc_marker_over_other_numbers() -> None:
    # "500g" appears first as a quantity; the real price is 29.9 Kč.
    name, price = parse_price("Tesco Oats 500g - 29.9 Kč")
    assert name == "Tesco Oats 500g"
    assert price == pytest.approx(29.9)


def test_parse_price_falls_back_to_last_number() -> None:
    # No "Kč" anywhere, so we take the last numeric token.
    name, price = parse_price("Mystery Item 200g 45")
    assert price == pytest.approx(45.0)
    assert name == "Mystery Item 200g"
