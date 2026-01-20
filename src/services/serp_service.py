from src.db.db import SessionLocal
from src.db.models import Product
from src.integrations.gpt import message_to_gpt
from src.integrations.serp_api import serp_search
from src.exceptions.exceptions import InvalidSearchResult
from asyncio import to_thread
import asyncio
from sqlalchemy import select, delete

from src.prompts import snippet_price_search, shopping_list,  get_recipe_from_gpt
from src.schemas.serp import SerpResults

def get_price(product: str) -> list[tuple]:
    """
    Fuction uses serp_api to scrap google search for product,
    :param product:str - a general name for the product
    :return:prices:list[teple] - a list max 3 tuples that have a tittle of the product
    in tesco and price that was found in serp_api json result
    """
    prices: list[tuple[str, str]] = []
    i = 0
    results:SerpResults = serp_search(product)
    # print (results)
    try:
        max_products_ammount = len(results.organic_results)
    except KeyError as e:  # Does this count as custom exception EDIKU?
        raise InvalidSearchResult("Invalid product name for Serp API") from e
    # print (max_products_ammount)

    while len(prices) < 3 and i < max_products_ammount:
        item = results.organic_results[i]
        title:str = item.title

        if item.rich_snippet and item.rich_snippet.bottom and item.rich_snippet.bottom.detected_extensions:
            price = item.rich_snippet.bottom.detected_extensions.price
        else:
            snippet = results.organic_results[i].snippet
            price = snippet_price_search(product, snippet)# GPT search for price in snippet
            if price in ("GPT + SERP: no price", "GPT + SERP: no price."):
                i += 1
                continue

        prices.append((title, price))
        i+=1

    # print(product)#TODO DELETE THIS
    # print(prices)#TODO DELETE THIS

    return prices



async def get_price_async(product: str):
    return await to_thread(get_price, product)


