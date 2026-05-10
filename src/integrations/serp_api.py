"""SerpAPI Google Search wrapper, scoped to Tesco Czech Republic."""

from serpapi import GoogleSearch

from src.config.settings import SERP_KEY
from src.schemas.serp import SerpResults


def serp_search(product: str) -> SerpResults:
    """Search Tesco's Czech site for a product and return parsed results.

    The query is restricted to ``site:nakup.itesco.cz`` so we get genuine
    Tesco product pages rather than blog posts or aggregators.

    Args:
        product: Czech product name to search for.

    Returns:
        Parsed ``SerpResults`` with at most a few organic hits.
    """
    params = {
        "engine": "google",
        "q": f"Tesco {product} price site:nakup.itesco.cz",
        "location": "Prague, Czechia",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "cz",
        "api_key": SERP_KEY,
    }

    raw_data = GoogleSearch(params).get_dict()
    return SerpResults(**raw_data)
