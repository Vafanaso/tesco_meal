"""End-to-end test of ``seed`` against an in-memory SQLite database."""

from sqlalchemy import select

from src.db import db as db_module
from src.db.models import Base, Product
from src.services import full_product_search


async def _reset_schema() -> None:
    """Drop and recreate all tables on the test (sqlite) engine."""
    async with db_module.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def test_seed_replaces_existing_rows_and_parses_prices() -> None:
    await _reset_schema()

    async with db_module.SessionLocal() as session:
        session.add(Product(name="leftover", price=999.0))
        await session.commit()

    await full_product_search.seed(
        [
            "Tesco Oats 500g, 29.9 Kč",
            "Banán - 25 Kč",
            "no price item",
        ]
    )

    async with db_module.SessionLocal() as session:
        rows = (await session.execute(select(Product))).scalars().all()

    by_name = {p.name: p for p in rows}
    assert "leftover" not in by_name
    assert by_name["Tesco Oats 500g"].price == 29.9
    assert by_name["Banán"].price == 25.0
    assert by_name["no price item"].price is None
    assert all(p.bought is False for p in rows)


async def test_seed_with_empty_list_clears_table() -> None:
    await _reset_schema()

    async with db_module.SessionLocal() as session:
        session.add(Product(name="ghost", price=1.0))
        await session.commit()

    await full_product_search.seed([])

    async with db_module.SessionLocal() as session:
        rows = (await session.execute(select(Product))).scalars().all()

    assert rows == []
