"""Environment-driven configuration loaded from a local ``.env`` file."""

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
OPENAI_KEY: str | None = os.getenv("OPENAI_API_KEY")
SERP_KEY: str | None = os.getenv("SERP_API_KEY")
DB_URL: str | None = os.getenv("DB_URL")
DB_LOCALHOST: str | None = os.getenv("DB_LOCALHOST")
