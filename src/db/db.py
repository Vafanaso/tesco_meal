from src.config.settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.db.models import Base

engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
