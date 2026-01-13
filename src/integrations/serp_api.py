from serpapi import GoogleSearch
from src.config.settings import SERP_KEY
from src.schemas.serp import SerpResults

API = SERP_KEY


def serp_search(product: str) -> SerpResults:
    params = {
        "engine": "google",
        "q": f"Tesco {product} price site:nakup.itesco.cz",
        "location": "Prague, Czechia",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "cz",
        "api_key": API,
    }

    search = GoogleSearch(params)
    raw_data = search.get_dict()
    results = SerpResults(**raw_data)
    return results

