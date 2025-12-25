from sqlalchemy import String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Product (Base):
    __tablename__ = "product_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable= False)
    price: Mapped[float] = mapped_column(Float, nullable= False)