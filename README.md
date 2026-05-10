# AI Budget Meal Planner – Telegram Bot

A Telegram bot that turns a daily budget into a complete meal plan and a
priced shopping list, using OpenAI for reasoning and (optionally) SerpAPI to
look up real Tesco product prices in the Czech Republic.

The bot drives the user through a short flow:

1. `/start` → choose a budget tier (**Cheap / Normal / Snob**).
2. Choose how many days to plan for (**1 / 2 / 3**).
3. The bot calls OpenAI to generate a recipe and a Czech grocery list with
   approximate prices in CZK.
4. The list is stored in PostgreSQL and rendered as an inline keyboard so the
   user can tick items off as they shop. The estimated total is shown in the
   message header.

---

## Features

- Budget-tier meal planning (`cheap` / `normal` / `snob`)
- AI-generated recipes (OpenAI Responses API, `gpt-5-nano`)
- Czech-language ingredient list with per-item price estimates
- Two price-resolution backends:
  - **GPT-only** (default; no SerpAPI quota required)
  - **SerpAPI + GPT** (real Tesco hits, enabled by switching one call in
    `src/handlers/menu.py`)
- Interactive inline shopping list with check/uncheck buttons
- Persistent storage in PostgreSQL via SQLAlchemy async + Alembic migrations
- Fully containerised with Docker Compose

---

## Requirements

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) for dependency management
- A PostgreSQL instance (the supplied `docker-compose.yaml` provides one)
- API keys for:
  - **Telegram Bot** (BotFather)
  - **OpenAI**
  - **SerpAPI** (only required if you switch to the SerpAPI flow)

---

## Configuration

Create a `.env` file in the project root (it is gitignored):

```dotenv
BOT_TOKEN=123456:ABC...
OPENAI_API_KEY=sk-...
SERP_API_KEY=...
DB_URL=postgresql+asyncpg://botuser:1258@db:5432/tesco_db
DB_LOCALHOST=postgresql+asyncpg://botuser:1258@localhost:5432/tesco_db
```

`DB_URL` is used by the bot when running inside the docker-compose network
(host = `db`). `DB_LOCALHOST` is used by Alembic when running migrations from
the host (host = `localhost`).

---

## Usage

### Run with Docker Compose (recommended)

```bash
docker compose up --build
```

This brings up Postgres and the bot. On first start, `init_db()` creates the
tables automatically (no Alembic step needed for development).

### Run locally

```bash
uv sync
uv run alembic upgrade head        # apply migrations
uv run python -m src.main          # start the bot
```

### Run the tests

```bash
uv run pytest
```

The test suite uses an in-memory SQLite database and mocks every external
call (OpenAI, SerpAPI), so it requires no API keys or network access.

---

## Architecture

```
src/
  main.py                 # entry point: init_db + start_polling
  config/settings.py      # .env loader
  integrations/
    bot.py                # shared aiogram Bot instance
    gpt.py                # thin OpenAI Responses client
    serp_api.py           # SerpAPI Google Search wrapper
  schemas/serp.py         # Pydantic models for the SerpAPI envelope
  prompts.py              # snippet→price prompt
  services/
    gpt_service.py        # recipe + shopping list + product picker prompts
    serp_service.py       # SerpAPI price lookup
    full_product_search.py# orchestration: GPT-only or SerpAPI+GPT search,
                          # plus seed() that wipes & repopulates the DB
  utils/price.py          # parse "Name, 29.9 Kč"-style strings
  db/
    models.py             # Product (id, name, price, bought)
    db.py                 # async engine + SessionLocal
  handlers/menu.py        # FSM: choosing_type → choosing_days → processing
                          #      → products_listing
  keyboards/keyboards.py  # reply + inline keyboards
  exceptions/exceptions.py# InvalidSearchResult
alembic/                  # database migrations
tests/                    # pytest suite (mocked APIs, sqlite)
```

### Data flow

```
user budget + days
        │
        ▼
get_recipe_from_gpt ──► (recipe text)
        │
        ▼
get_shopping_list ───► ["Tesco Oats 500g - 29 Kč", "Banán - 25 Kč", ...]
        │
        ▼            (optional SerpAPI lookup per item)
parse_price ────────► [(name, price), ...]
        │
        ▼
seed() wipes Product, inserts new rows
        │
        ▼
products_keyboard renders inline buttons; toggle_product flips `bought`
```

### Budget handling

Budget tracking works in two layers:

- stores a numeric `price` column on `Product`,
- extracts the price from the GPT/SerpAPI response strings via
  `src.utils.price.parse_price` (handles `29 Kč`, `2,69 Kč`, `25-35 Kč`,
  bare numbers, and missing prices),
- shows the running total in the shopping-list message header,
- treats unparseable prices as `NULL` rather than `0` so they don't silently
  understate the total.

The budget *tier* (cheap/normal/snob) is communicated to GPT in the prompt
as a CZK/day guideline. Strict post-hoc enforcement (e.g. trimming the list
when the total exceeds the tier) is intentionally out of scope for now and
documented as future work.

---

## Tech stack

- Python 3.12
- [aiogram 3](https://aiogram.dev/) for the Telegram interface
- [openai](https://github.com/openai/openai-python) (Responses API, `gpt-5-nano`)
- [google-search-results](https://github.com/serpapi/google-search-results-python) (SerpAPI)
- [SQLAlchemy 2 async](https://docs.sqlalchemy.org/) + [asyncpg](https://magicstack.github.io/asyncpg/) + [Alembic](https://alembic.sqlalchemy.org/)
- [pydantic 2](https://docs.pydantic.dev/) for SerpAPI response validation
- [python-dotenv](https://github.com/theskumar/python-dotenv) for `.env` loading
- [pytest](https://docs.pytest.org/) + [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) + [aiosqlite](https://github.com/omnilib/aiosqlite) for the test suite
- [uv](https://docs.astral.sh/uv/) for dependency management

---

## Future work

- Switch the OpenAI shopping-list prompt to a JSON schema so the price field
  is structured rather than parsed out of free text.
- Persist completed `Recipe` rows so users can browse history.
- Enforce the budget tier strictly: trim or replace items when the running
  total exceeds the per-day allowance.
