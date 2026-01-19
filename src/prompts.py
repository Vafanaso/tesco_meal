from src.integrations.gpt import message_to_gpt
def snippet_price_search (product: str, snippet:str):
    res = message_to_gpt(f"I am sending you a snippet regarding {product}. "
                f"Find a price and send ONLY numbers + Kč. "
                f"If no price, return exactly: GPT + SERP: no price. "
                f"Snippet: {snippet}")
    return res

def shopping_list(recipe:str) -> str:
    initial_products = message_to_gpt(
        f"give me a list of groceries for this recipe {recipe}, give me only products, without the prices, "
        f" all i need is a list of products divided by coma, the names of the product should be in czech and readable for example not červenáčočka but červená čočka, "

    )
    return initial_products

def get_recipe_from_gpt(type:str, number_of_days:int) -> str:
    recipe = message_to_gpt(f'I want to cook something, your task is to give me a {type} recipe for {number_of_days} days,, if the type is budget,'
                            f' i am willing to spend around 150 czech krouns for a day,for normal 300 czech krouns per day, and snob 500+ per day or two.'
                            f' please, answer this message with only a recipe and meals description, the recipe shouldnt be longer that 3500 chars')
    return recipe

# def choosing_from_3products(products:list[tuple], product_name:str) -> str:
