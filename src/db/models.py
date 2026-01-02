from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Product (Base):
    __tablename__ = "product_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable= False)
    bought: Mapped[bool] = mapped_column(Boolean, default=False)

    #price: Mapped[str] = mapped_column(String(10), nullable= False)