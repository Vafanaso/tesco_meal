from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List



class Base(DeclarativeBase):
    pass

recipe_product = Table(
    "recipe_product",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key= True),
    Column("product_id", ForeignKey("product_info.id"), primary_key=True)
)


class Product(Base):
    __tablename__ = "product_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bought: Mapped[bool] = mapped_column(Boolean, default=False)

    recipes: Mapped[List["Recipe"]] = relationship(secondary=recipe_product, back_populates='products')

    # price: Mapped[str] = mapped_column(String(10), nullable= False)
class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description:Mapped[str] = mapped_column(String(3500), nullable=False)

    products: Mapped[List["Product"]] = relationship(secondary=recipe_product, back_populates='recipes')