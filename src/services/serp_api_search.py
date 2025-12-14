from pyexpat.errors import messages
from src.integrations.gpt import message_to_gpt
from src.integrations.serp_api import serp_search

# float for prices
# custom exceptions in python

def get_price(product:str) ->list|str:
    prices:list[str] = []
    results:dict= serp_search(product)
    print (results)
    try:
        organic_results = results["organic_results"]
    except KeyError:
        return 'Invalid input, please try rephrasing kurwa'

    for i in range (4):
        res:tuple = ()
        try:
            tittle = results['organic_results'][i]['title']
        except IndexError:
            break

        try:
            price = f'{results['organic_results'][i]['rich_snippet']['bottom']['detected_extensions']['price']} Kč'
        except KeyError:
            price = "No price found by serp_api"
        except TypeError:
            price = "No price found by serp_api"


        if price == 'No price found by serp_api':
            try:
                gpt_price_search = results['organic_results'][i]['snippet']
            except KeyError:
                return 'Invalid input, please try rephrasing kurwa'
            price = message_to_gpt(f'I am sending you a snippet of the information regarding {product}, please find a price and send me  the numbers, '
                f'no additional information is needed, ONLY the numbers of the price + Kč if you will find them, if you have a lot of optioan, '
                        f'for example there are prices for different weight, then your goal is to give a price that is closer to 500grams,'
                        f' and give an answer like 45Kc/0.5Kg and /0.5l for liquids, price is of course on you, i want you do be flexible in seeing the price, if you see that the price is in pounds, then just say GPT + SERP: no price.'
                f' If there is no price, send ONLY the text (GPT + SERP: no price), here is the snippet {gpt_price_search}'
                )


        res = (tittle, price)
        if res[1] != 'GPT + SERP: no price':
            prices.append(res)
    return prices


def get_shopping_list(max_money:str) ->list:
    products:list = []
    tem_prod:list = []
    initial_products =  message_to_gpt(f'give me a list of groceries for {max_money}czk, give me only products, without the prices, '
                          f'you should make a list approximately for this ammount of money, but keep prices to yourself,'
                          f' all i need is a list of products devided by coma, the names of the product should be in czech')
    for char in initial_products:
        if char not in [',', ' ']:
            tem_prod.append(char)
        elif char == ',':
            products.append(''.join(tem_prod))
            tem_prod = []
        elif char == ' ':
            continue
    print(products)
    return products

# new_prod:list = get_shopping_list('400')
# for item in new_prod