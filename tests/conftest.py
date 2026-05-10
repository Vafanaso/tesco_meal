"""Test bootstrap: fake env vars so ``src.config.settings`` imports cleanly."""

import os

os.environ.setdefault("BOT_TOKEN", "0:test")
os.environ.setdefault("OPENAI_API_KEY", "sk-test")
os.environ.setdefault("SERP_API_KEY", "test")
os.environ.setdefault("DB_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("DB_LOCALHOST", "sqlite+aiosqlite:///:memory:")
