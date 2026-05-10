"""Async SQLAlchemy engine and session factory."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config.settings import DB_URL
from src.db.models import Base


def _async_url(raw: str | None) -> str:
    """Coerce a plain Postgres URL to the asyncpg-aware form.

    ``.env`` files are usually written with the bare ``postgresql://...``
    form (what ``psql`` / ``psycopg2`` / Alembic expect), but
    ``create_async_engine`` needs a driver-prefixed URL such as
    ``postgresql+asyncpg://...``. We normalise here so users can keep one
    URL in ``.env`` and the bot still starts.

    Args:
        raw: The configured database URL, possibly missing a driver prefix.

    Returns:
        An async-driver-prefixed URL, or the input unchanged if it already
        specifies a driver (e.g. ``sqlite+aiosqlite://`` for tests).

    Raises:
        RuntimeError: If ``raw`` is empty - misconfiguration we'd rather
            surface immediately than fail on first query.
    """
    if not raw:
        raise RuntimeError(
            "DB_URL is not set. Configure it in .env (see README.md)."
        )
    if raw.startswith("postgresql://"):
        return "postgresql+asyncpg://" + raw[len("postgresql://") :]
    return raw


engine = create_async_engine(_async_url(DB_URL), echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    """Create all tables that do not yet exist.

    Used in development. In production we run Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
