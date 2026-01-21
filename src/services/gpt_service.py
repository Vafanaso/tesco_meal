from src.db.db import SessionLocal
from src.db.models import Product
from src.integrations.gpt import message_to_gpt
from src.integrations.serp_api import serp_search
from src.exceptions.exceptions import InvalidSearchResult
from asyncio import to_thread
import asyncio
from sqlalchemy import select, delete


from src.schemas.serp import SerpResults
#-------------------------------------------------------------------------------------
#------------------------------- SERP DRIVEN FUNCTIONS -------------------------------
#-------------------------------------------------------------------------------------

def serp_snippet_price_search (product: str, snippet:str):
    res = message_to_gpt(f"I am sending you a snippet regarding {product}. "
                f"Find a price and send ONLY numbers + Kč. "
                f"If no price, return exactly: GPT + SERP: no price. "
                f"Snippet: {snippet}")
    return res


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



#-----------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------- PURE GPT DRIVEN FUNCTIONS -------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------


# def get_recipe_from_gpt(budget:str, number_of_days:int) -> tuple[str,str]:
#     """
#     function makes a recipe with chatgpt
#     :param budget: a type of recipe, for ex (cheap, normal, snob - expensive).
#     :param number_of_days:int - a number of days that recipe should be done for
#     :return: tuple of name of the recipe and the recipe itself
#     """
#     recipe = message_to_gpt(f'I want to cook something new i already have this recepies, your task is to give me a {budget} recipe for {number_of_days} days,, if the type is cheep,'
#                             f' i am willing to spend around 150 czech krouns for a day,for normal 300 czech krouns per day, and snob 500+ per day or two.'
#                             f' please, answer this message with only a recipe and meals description, the recipe shouldnt be longer that 3500 chars, '
#                             f'THE BEGING OF THE RECIPE HAS TO BE A SHORT SENTENCE WHERE YOU WILL SAY THE NAMES OF THE MEALS DEVIDED BY COMA, '
#                             f'for example Goulash, Chicken steak with bulgur, Greek yogurt with berries.')
#
#     name_temp:list =[]
#     for char in recipe:
#         if char == '.':
#             break
#         name_temp.append(char)
#     name = ''.join(name_temp)
#     return name, recipe


def get_recipe_from_gpt(budget: str, number_of_days: int) -> tuple[str, str]:
    """
    function makes a recipe with chatgpt
    :param budget: a type of recipe, for ex (cheap, normal, snob - expensive).
    :param number_of_days:int - a number of days that recipe should be done for
    :return: tuple of name of the recipe and the recipe itself
    """

    prompt = (
        f"I want a {budget} recipe for {number_of_days} days. "
        f"Budget guidelines: cheap (~150 CZK/day), normal (~300 CZK/day), snob (500+ CZK/day). "
        f"Format: The VERY FIRST line must be only the names of the meals divided by commas. "
        f"Followed by the full recipe and description (max 3500 chars)."
    )

    recipe_content = message_to_gpt(prompt)

    # Split by newline to get the first line (the names)
    lines = recipe_content.strip().split('\n')
    name = lines[0] if lines else "New Recipe"

    return name, recipe_content




async def shopping_list(recipe:str, session) -> str:

    exising_products = await session.execute(select(Product.full_name, Product.id))
    exising_products_list = exising_products.all()
    initial_products = message_to_gpt(
        f"give me a list of groceries for this recipe {recipe}, give me only products, without the prices, "
        f" all i need is a list of products and their aproximate prices, divided by coma, the names of the product should be in czech"
        f" and readable for example not červenáčočka but červená čočka. "
        f"Examle of correct answer = Ovesné vločky jemné – 1 kg: 29 Kč, Banán – 29 Kč/kg, Tesco Skořice mletá 40 g – 14 Kč "
        f"Before trying to come up with a product that is needed for the recipe, try to find in this list of products and their ids {exising_products_list},"
        f" if it is there, just take its id, if you dont see anything fitting, give a new one, now lets say that from previous example you found that Ovesné vločky jemné "
        f"are in the list that i gave you, and it has an id 4, so now the correct answer will be  4, Banán – 29 Kč/kg, Tesco Skořice mletá 40 g – 14 Kč "

    )
    return initial_products


def get_shopping_list(recipe: str, session) -> list[str]:
    """
    Uses function shopping_list to get a list of products or id;s and then makes it into python list
    :param session: - db session
    :param recipe:str - a recipe for meals
    :return: products:list[str] - list of products that you should buy
    """
    initial_products = shopping_list(recipe, session)

    # This replaces the 'for char in initial_products' loop
    # 1. split(",") breaks the string into a list at every comma
    # 2. .strip() removes leading/trailing spaces but keeps spaces BETWEEN words
    # 3. 'if item.strip()' ensures no empty strings are added to the list
    products = [item.strip() for item in initial_products.split(",") if item.strip()]

    # print(products)  # TODO DELETE THIS
    return products



