import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
load_dotenv()

API = os.getenv("SERP_API_KEY")


def serp_search(product:str) ->dict:
    res_list:list = []
    params = {
      "engine": "google",
      "q": f"Tesco {product} price site:nakup.itesco.cz",
      "location": "Prague, Czechia",
      "google_domain": "google.com",
      "hl": "en",
      "gl": "cz",
      "api_key": API
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results