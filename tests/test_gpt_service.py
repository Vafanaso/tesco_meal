"""Unit tests for ``src.services.gpt_service`` with the OpenAI call mocked."""

from unittest.mock import patch

from src.services import gpt_service


def test_get_shopping_list_splits_on_commas() -> None:
    fake_response = "Ovesné vločky 500 g - 29 Kč, Banán - 25 Kč, Sůl - 12 Kč"
    with patch.object(gpt_service, "shopping_list", return_value=fake_response):
        items = gpt_service.get_shopping_list("any recipe text")

    assert items == [
        "Ovesné vločky 500 g - 29 Kč",
        "Banán - 25 Kč",
        "Sůl - 12 Kč",
    ]


def test_get_shopping_list_drops_empty_segments() -> None:
    with patch.object(gpt_service, "shopping_list", return_value=" a , , b , "):
        assert gpt_service.get_shopping_list("recipe") == ["a", "b"]


def test_get_recipe_from_gpt_returns_first_line_as_name() -> None:
    fake = "Goulash, Chicken bulgur, Yogurt\n\nDay 1\nBreakfast: ...\n"
    with patch.object(gpt_service, "message_to_gpt", return_value=fake):
        name, recipe = gpt_service.get_recipe_from_gpt("normal", "2")

    assert name == "Goulash, Chicken bulgur, Yogurt"
    assert recipe == fake


def test_get_recipe_from_gpt_handles_empty_response() -> None:
    with patch.object(gpt_service, "message_to_gpt", return_value=""):
        name, recipe = gpt_service.get_recipe_from_gpt("cheap", "1")

    assert name == "New Recipe"
    assert recipe == ""


def test_choosing_right_product_with_options_uses_list_prompt() -> None:
    captured: dict[str, str] = {}

    def fake_gpt(prompt: str) -> str:
        captured["prompt"] = prompt
        return "Tesco Oats 500g, 29.9"

    options = [("Tesco Oats 500g", 29.9), ("Other Oats 1kg", 49.9)]
    with patch.object(gpt_service, "message_to_gpt", side_effect=fake_gpt):
        result = gpt_service.choosing_right_product(options, "ovesné vločky")

    assert result == "Tesco Oats 500g, 29.9"
    assert "Tesco Oats 500g" in captured["prompt"]
    assert "ovesné vločky" in captured["prompt"]


def test_choosing_right_product_with_no_options_uses_fallback() -> None:
    with patch.object(
        gpt_service, "message_to_gpt", return_value="rýže, 35 Kč"
    ):
        result = gpt_service.choosing_right_product([], "rýže")

    assert result.endswith(" last resort GPT")
    assert "rýže" in result
