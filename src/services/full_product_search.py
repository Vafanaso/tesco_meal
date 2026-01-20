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
from src.services.gpt_service import choosing_right_product_async, get_shopping_list, get_prices_gpt
from src.services.serp_service import get_price_async


# float for prices
# custom exceptions in python
# prompts to file
#TODO same result all the time, work with db
#TODO long product names



# async def get_price_async(product: str):
#     return await to_thread(get_price, product)

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

# def get_shopping_list(recipe: str) -> list[str]:
#     """
#     fucntion takes a recipe and asks gpt and gives a list of products for this recipe
#     :param recipe:str - a recipe for meals
#     :return: products:list[str] - list of products that you should buy
#     """
#     initial_products = shopping_list(recipe)
#
#     # This replaces the 'for char in initial_products' loop
#     # 1. split(",") breaks the string into a list at every comma
#     # 2. .strip() removes leading/trailing spaces but keeps spaces BETWEEN words
#     # 3. 'if item.strip()' ensures no empty strings are added to the list
#     products = [item.strip() for item in initial_products.split(",") if item.strip()]
#
#     # print(products)  # TODO DELETE THIS
#     return products


# def choosing_right_product(
#     list_of_product_and_prices: list[tuple[str, str]], product: str
# ) -> str:
#
#     if len(list_of_product_and_prices) != 0:
#         prompt = (
#             f"here is the list of products and prices{list_of_product_and_prices}, i want you to choose the best option, "
#             f"that you find the ,ost realistic and fiting to the initial search, which is {product}. "
#             f"The answer from you should be strictly a string with the name and price devided by coma, "
#             f"you can not take the name nor the price from anywhere else but the list that I gave you. and be carefull, voda is not a vodka  "
#         )
#         best_pick: str = message_to_gpt(prompt)
#     else:  # THE LAST BASTION TO FIND THE PRICE
#         prompt = (
#             f" I want to buy {product} in Tesco store in Prague, Czech Republic, please tell me the approximate price for it"
#             f"The answer from you should be strictly a string with the name and price devided by coma, "
#             f"you can not take the name  from anywhere else but the name that I gave you.  "
#         )
#         best_pick: str = message_to_gpt(prompt) + " last resort GPT"
#
#     # print(best_pick)#TODO DELETE
#
#     return best_pick


# async def choosing_right_product_async(
#     list_of_product_and_prices: list[tuple[str, str]], product: str
# ):
#     return await to_thread(choosing_right_product, list_of_product_and_prices, product)


# def full_search(monney:str) ->list[str]:
#     full_shop_list:list= get_shopping_list(monney)
#     final_list:list = []
#     for item in full_shop_list:
#         prod_options:list[tuple]= get_price(item)
#         best_pick= choosing_right_product(prod_options, item)
#         final_list.append(best_pick)
#     return final_list


async def process_product(product: str) -> str:
    prod_options = await get_price_async(product)
    best_pick = await choosing_right_product_async(prod_options, product)
    return best_pick


async def full_search_async_serp(type:str, number_of_days:int) -> tuple[str,list[str]]:
    recipe = get_recipe_from_gpt(type, number_of_days)


    full_shop_list = await to_thread(get_shopping_list, recipe)

    tasks = [process_product(item) for item in full_shop_list]

    results = await asyncio.gather(*tasks)

    # print(results)#TODO DELETE THIS
    return recipe, results

async def full_search_async_gpt(type:str, number_of_days:str) -> tuple[str,list[str]]:
    recipe = get_recipe_from_gpt(type, number_of_days)


    full_shop_list = await to_thread(get_shopping_list, recipe)

    # tasks = [to_thread(get_prices_gpt, item) for item in full_shop_list]
    # results = await asyncio.gather(*tasks)

    # print(results)#TODO DELETE THIS
    # print (full_shop_list)
    return recipe, full_shop_list


# asyncio.run(full_search_async_gpt('normal', '1'))


async def seed(products: list[str]):
    async with SessionLocal() as session:
        await session.execute(delete(Product))

        for item in products:
            session.add(Product(name=item))
        await session.commit()





# async def test_all():
#     await full_search_async("cheep", 2)
#
# asyncio.run(test_all())
"""
Output N1


{'https://serpapi.com/searches/9f4dd658060e8a18/693f02a29f8abc1d670e5375.json',
"""

"""Day 1

Breakfast: Oats with banana and peanut butter
- Ingredients: 1 cup rolled oats, 2 cups water or milk, 1 banana, 1–2 tbsp peanut butter, pinch of cinnamon (optional)
- Steps: In a pot, bring water/milk to a boil. Add oats; simmer 5–7 minutes until thick. Stir in sliced banana and peanut butter. Sprinkle with cinnamon if desired.

Lunch: Simple lentil soup
- Ingredients: 1 cup red or green lentils, 1 small onion (diced), 1 carrot (diced), 2 cloves garlic (minced), 1 can crushed tomatoes (400 g), 4 cups vegetable stock or water, salt, pepper, 1/2 tsp cumin, 1/2 tsp paprika, 1 tbsp oil
- Steps: Sauté onion and carrot in oil until soft. Add garlic 1 minute. Stir in lentils, tomatoes, stock, and spices. Simmer 25–30 minutes until lentils are tender. Season to taste.

Dinner: Rice with beans and roasted veg
- Ingredients: 1 cup rice (uncooked), 1 can beans (400 g), 1 small onion (sliced), 1 bell pepper (diced), 2 cloves garlic (minced), 1/2 tsp cumin, 1/2 tsp chili powder, 1 tbsp oil, salt, pepper
- Steps: Cook rice according to package. Sauté onion, pepper, and garlic in oil until soft. Add beans and spices; warm through. Serve bean mix over rice.

Day 2

Breakfast: Tomato egg toast
- Ingredients: 4 slices bread, 4 eggs, 2 tomatoes (sliced), 1–2 tsp oil or butter, salt, pepper
- Steps: Toast bread. Sauté or fry eggs to desired doneness. Top toast with tomato slices, add eggs on top or side, season with salt and pepper.

Lunch: Reheated lentil soup (leftovers from Day 1)
- Steps: Gently reheat lentil soup on stovetop or microwave. Serve with a slice of bread or a simple side salad if available.

Dinner: Potato chickpea curry with rice
- Ingredients: 2 large potatoes (cubed), 1 can chickpeas (drained), 1 can tomatoes (400 g), 1 onion (chopped), 2 cloves garlic (minced), 1–2 tbsp curry powder, 1 tbsp oil, salt, pepper, 1 cup rice (uncooked)
- Steps: Cook rice according to package. Sauté onion and garlic in oil until fragrant. Add curry powder and toast 1 minute. Stir in potatoes, tomatoes, and 1 cup water; simmer until potatoes are tender (about 15–20 minutes). Add chickpeas; heat through. Season and serve with rice.
['ovesnévločky', 'voda', 'mléko', 'banán', 'arašídovémáslo', 'skořice', 'červenáčočka', 'zelenáčočka', 'cibule', 'mrkev', 'česnek', 'drcenárajčata', 'zeleninovývývar', 'sůl', 'pepř', 'římskýkmín', 'paprika', 'olej', 'fazole', 'paprikasladká', 'chilliprášek', 'rýže', 'chléb', 'vejce', 'rajčata', 'brambory', 'cizrna', 'kariprášek']


['Emco Oatmeal Fine Wholegrain 500g, 29.9', 'Pražská Original Vodka 0.5L, 149.9 Kč', 'Trvanlivé mléko - Tesco Groceries, 12,90 Kč', 'Tesco Banana Chips 100g,24.9', '4Slim Arašídové máslo s belgickou čokoládou 500g, 224.9', 'Kotányi Skořice mletá 25g - Tesco Groceries, 25.9 Kč', 'Tesco Organic Red Whole Lentils 500g, 51.9', 'Tesco Green Lentils 500g, 33.9', 'Cibule - Tesco Groceries,2,69 Kč', 'Tesco Carrot Bundle,19.9', 'Česnek - Tesco Groceries,8,96 Kč', 'Gustodoro Crushed Tomatoes 400g,53.9', 'Hami Meat and Vegetable Side Dish ...,49.9', 'Solné Mlýny Edible Sea Salt with Iodine 1kg,29.9', 'Vitana Pepř černý mletý 18g - Tesco Groceries, 21.9 Kč', 'Vitana Římský kmín celý 25g - Tesco Groceries,29.9', 'Tesco Yellow Paprika,23.98', 'Tesco Auto Motor Oil 5W-30 1L, 209.9', 'Tesco White Beans 500g,34.9', 'Kotányi Ground Sweet Paprika 30g, 15.9', 'Tesco Red Beans in Chilli Sauce 400g,17.9', 'Rýže - Tesco Groceries, 69,90 Kč', 'Tesco Sliced Bread 500g,37.9', 'Tesco Čerstvá vejce z podestýlky M 30 ks,229.9', 'Tesco Tomatoes Oval 500g,49.9', 'Tesco Potatoes 2.5kg, 79.9', 'Tesco Organic Chickpeas 500g, 62.9', 'kariprášek, 25-35 Kč last resort GPT']
"""
