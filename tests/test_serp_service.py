"""Unit tests for ``src.services.serp_service`` with SerpAPI/GPT mocked."""

from unittest.mock import patch

import pytest

from src.exceptions.exceptions import InvalidSearchResult
from src.schemas.serp import (
    Bottom,
    DetectedExtensions,
    OrganicResult,
    RichSnippet,
    SerpResults,
)
from src.services import serp_service


def _make_result(
    title: str,
    *,
    position: int = 1,
    snippet: str | None = None,
    price: float | None = None,
) -> OrganicResult:
    rich = None
    if price is not None:
        rich = RichSnippet(
            bottom=Bottom(detected_extensions=DetectedExtensions(price=price))
        )
    return OrganicResult(
        position=position, title=title, snippet=snippet, rich_snippet=rich
    )


def test_get_price_uses_rich_snippet_when_present() -> None:
    fake = SerpResults(
        organic_results=[_make_result("Tesco Oats 500g", price=29.9)]
    )
    with patch.object(serp_service, "serp_search", return_value=fake):
        result = serp_service.get_price("ovesné vločky")

    assert result == [("Tesco Oats 500g", 29.9)]


def test_get_price_falls_back_to_snippet_extraction() -> None:
    fake = SerpResults(
        organic_results=[
            _make_result("Tesco Oats 500g", snippet="some text 29.9 Kč today")
        ]
    )
    with (
        patch.object(serp_service, "serp_search", return_value=fake),
        patch.object(
            serp_service, "snippet_price_search", return_value="29.9 Kč"
        ),
    ):
        result = serp_service.get_price("ovesné vločky")

    assert result == [("Tesco Oats 500g", "29.9 Kč")]


def test_get_price_skips_results_with_no_price_signal() -> None:
    fake = SerpResults(
        organic_results=[
            _make_result("No Price Item", position=1, snippet="x"),
            _make_result("Tesco Oats 500g", position=2, price=29.9),
        ]
    )
    with (
        patch.object(serp_service, "serp_search", return_value=fake),
        patch.object(
            serp_service,
            "snippet_price_search",
            return_value="GPT + SERP: no price",
        ),
    ):
        result = serp_service.get_price("ovesné vločky")

    assert result == [("Tesco Oats 500g", 29.9)]


def test_get_price_caps_at_three_results() -> None:
    fake = SerpResults(
        organic_results=[
            _make_result(f"Item {i}", position=i, price=float(i))
            for i in range(1, 6)
        ]
    )
    with patch.object(serp_service, "serp_search", return_value=fake):
        result = serp_service.get_price("anything")

    assert len(result) == 3
    assert [title for title, _ in result] == ["Item 1", "Item 2", "Item 3"]


def test_get_price_returns_empty_when_no_organic_results() -> None:
    fake = SerpResults(organic_results=[])
    with patch.object(serp_service, "serp_search", return_value=fake):
        assert serp_service.get_price("blah") == []


def test_get_price_raises_when_serp_response_is_malformed() -> None:
    class Broken:
        @property
        def organic_results(self) -> list[OrganicResult]:
            raise KeyError("organic_results")

    with patch.object(serp_service, "serp_search", return_value=Broken()):
        with pytest.raises(InvalidSearchResult):
            serp_service.get_price("anything")
