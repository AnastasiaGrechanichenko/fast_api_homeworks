
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "store_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    age: Mapped[int]
    password: Mapped[str]

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    author: Mapped[str]
    price: Mapped[int]
    old_price: Mapped[int]
    image: Mapped[str]
    category:Mapped[str]

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="book")

class CartItem(Base):
    __tablename__ = "cart_items"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("store_users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped["User"] = relationship(back_populates="cart_items")
    book:Mapped["Book"] = relationship(back_populates="cart_items")



