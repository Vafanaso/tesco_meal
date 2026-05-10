"""Tests for the SerpAPI Pydantic envelope."""

from src.schemas.serp import OrganicResult, SerpResults


def test_serp_results_accepts_minimal_payload() -> None:
    result = SerpResults(**{})
    assert result.organic_results == []


def test_serp_results_parses_organic_results() -> None:
    result = SerpResults(
        organic_results=[
            {
                "position": 1,
                "title": "Tesco Oats 500g",
                "snippet": "Some snippet",
                "rich_snippet": {
                    "bottom": {"detected_extensions": {"price": 29.9}}
                },
            }
        ]
    )
    assert isinstance(result.organic_results[0], OrganicResult)
    assert result.organic_results[0].title == "Tesco Oats 500g"
    assert (
        result.organic_results[0].rich_snippet.bottom.detected_extensions.price
        == 29.9
    )


def test_serp_results_tolerates_missing_optional_fields() -> None:
    result = SerpResults(
        organic_results=[{"position": 1, "title": "Bare Result"}]
    )
    only = result.organic_results[0]
    assert only.snippet is None
    assert only.rich_snippet is None
    assert only.link is None
