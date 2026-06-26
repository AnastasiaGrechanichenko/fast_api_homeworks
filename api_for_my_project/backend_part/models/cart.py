from sqlalchemy import ForeignKey

from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CartItem(Base):
    __tablename__ = "cart_items"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("store_users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped["User"] = relationship(back_populates="cart_items")
    book:Mapped["Book"] = relationship(back_populates="cart_items")