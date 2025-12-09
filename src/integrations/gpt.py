from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def message_to_gpt(message:str):
    response = client.responses.create(
        model="gpt-5-nano",
        input=message
    )
    return response.output_text