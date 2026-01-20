from src.db.db import SessionLocal
from src.db.models import Product
from src.integrations.gpt import message_to_gpt
from src.integrations.serp_api import serp_search
from src.exceptions.exceptions import InvalidSearchResult
from asyncio import to_thread
import asyncio
from sqlalchemy import select, delete


from src.schemas.serp import SerpResults


def snippet_price_search (product: str, snippet:str):
    res = message_to_gpt(f"I am sending you a snippet regarding {product}. "
                f"Find a price and send ONLY numbers + Kč. "
                f"If no price, return exactly: GPT + SERP: no price. "
                f"Snippet: {snippet}")
    return res


def get_recipe_from_gpt(type:str, number_of_days:int) -> str:
    """
    function makes a recipe with chatgpt
    :param recipe_option: a type of recipe, for ex (budget- cheap, normal, snob - expensive).
    :param number_of_days:int - a number of days that recipe should be done for
    :return: recipe:str - a recipe for the meals
    """
    recipe = message_to_gpt(f'I want to cook something, your task is to give me a {type} recipe for {number_of_days} days,, if the type is budget,'
                            f' i am willing to spend around 150 czech krouns for a day,for normal 300 czech krouns per day, and snob 500+ per day or two.'
                            f' please, answer this message with only a recipe and meals description, the recipe shouldnt be longer that 3500 chars')
    return recipe

# def get_recipe(recipe_option:str, number_of_days:int) -> str:
#     """
#     function makes a recipe with chatgpt
#     :param recipe_option: a type of recipe, for ex (budget- cheap, normal, snob - expensive).
#     :param number_of_days:int - a number of days that recipe should be done for
#     :return: recipe:str - a recipe for the meals
#     """
#     recipe = get_recipe_from_gpt(recipe_option, number_of_days)
#
#     #
#     # print(recipe)#TODO DELETE THIS
#
#     return recipe


def shopping_list(recipe:str) -> str:
    initial_products = message_to_gpt(
        f"give me a list of groceries for this recipe {recipe}, give me only products, without the prices, "
        f" all i need is a list of products and their aproximate prices, divided by coma, the names of the product should be in czech"
        f" and readable for example not červenáčočka but červená čočka. "
        f"Examle of correct answer = Ovesné vločky jemné – 1 kg: 29 Kč, Banán – 29 Kč/kg, Tesco Skořice mletá 40 g – 14 Kč "

    )
    return initial_products


def get_shopping_list(recipe: str) -> list[str]:
    """
    fucntion takes a recipe and asks gpt and gives a list of products for this recipe
    :param recipe:str - a recipe for meals
    :return: products:list[str] - list of products that you should buy
    """
    initial_products = shopping_list(recipe)

    # This replaces the 'for char in initial_products' loop
    # 1. split(",") breaks the string into a list at every comma
    # 2. .strip() removes leading/trailing spaces but keeps spaces BETWEEN words
    # 3. 'if item.strip()' ensures no empty strings are added to the list
    products = [item.strip() for item in initial_products.split(",") if item.strip()]

    # print(products)  # TODO DELETE THIS
    return products

def choosing_right_product(
    list_of_product_and_prices: list[tuple[str, str]], product: str
) -> str:

    if len(list_of_product_and_prices) != 0:
        prompt = (
            f"here is the list of products and prices{list_of_product_and_prices}, i want you to choose the best option, "
            f"that you find the ,ost realistic and fiting to the initial search, which is {product}. "
            f"The answer from you should be strictly a string with the name and price devided by coma, "
            f"you can not take the name nor the price from anywhere else but the list that I gave you. and be carefull, voda is not a vodka  "
        )
        best_pick: str = message_to_gpt(prompt)
    else:  # THE LAST BASTION TO FIND THE PRICE
        prompt = (
            f" I want to buy {product} in Tesco store in Prague, Czech Republic, please tell me the approximate price for it"
            f"The answer from you should be strictly a string with the name and price devided by coma, "
            f"you can not take the name  from anywhere else but the name that I gave you.  "
        )
        best_pick: str = message_to_gpt(prompt) + " last resort GPT"

    # print(best_pick)#TODO DELETE

    return best_pick


async def choosing_right_product_async(
    list_of_product_and_prices: list[tuple[str, str]], product: str
):
    return await to_thread(choosing_right_product, list_of_product_and_prices, product)


def get_prices_gpt(product:str) -> str:
    return message_to_gpt(f"Give me an approximate price for this product: {product} in czk,if the price is from tesco cz it is better,"
                          f" your answer has to be strictly a product name and price, also consider thinking about small amounts of a product,"
                          f" for example 100 g of cheeze or only 1 kg of potatoes and for example only 10 egs")


