from src.integrations.gpt import message_to_gpt
def snipet_price_search (product: str, snippet:str):
    res = message_to_gpt(f"I am sending you a snippet regarding {product}. "
                f"Find a price and send ONLY numbers + Kč. "
                f"If no price, return exactly: GPT + SERP: no price. "
                f"Snippet: {snippet}")
    return res