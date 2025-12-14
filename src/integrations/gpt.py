from openai import OpenAI
from src.config.settings import OPENAI_KEY

OPENAI_API_KEY = OPENAI_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

def message_to_gpt(message:str):
    response = client.responses.create(
        model="gpt-5-nano",
        input=message
    )
    return response.output_text