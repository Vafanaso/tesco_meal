"""SQLAlchemy ORM models for the bot's persistent state."""

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


class Product(Base):
    """One item on the user's current shopping list.

    Attributes:
        id: Primary key.
        name: Product display name as shown on the inline keyboard.
        price: Estimated price in CZK. ``None`` when no price could be
            extracted from the GPT/SerpAPI response - those products are
            skipped when computing the budget total.
        bought: Whether the user has ticked the item off the list.
    """

    __tablename__ = "product_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    bought: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
