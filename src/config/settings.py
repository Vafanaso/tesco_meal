import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
SERP_KEY = os.getenv("SERP_API_KEY")
DB_URL = os.getenv("DB_URL")
DB_LOCALHOST = os.getenv("DB_LOCALHOST")
