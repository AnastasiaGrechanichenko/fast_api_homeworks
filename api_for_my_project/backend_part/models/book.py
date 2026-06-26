from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    author: Mapped[str]
    price: Mapped[int]
    old_price: Mapped[int]
    image: Mapped[str]
    category:Mapped[str]