from datetime import datetime
from email.policy import default

from sqlalchemy import ForeignKey

from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("store_users.id"))
    total_sum:Mapped[int]
    total_discount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    status: Mapped[str] = mapped_column(default="pending")

    recipient_name:Mapped[str]=mapped_column(nullable=True,default="")
    phone:Mapped[str]=mapped_column(nullable=True,default="")
    address:Mapped[str]=mapped_column(nullable=True,default="")

    payment_status:Mapped[str]=mapped_column(nullable=True,default="pending")

    comment:Mapped[str]=mapped_column(nullable=True,default="")


    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id:Mapped[int] = mapped_column(ForeignKey("orders.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    title: Mapped[str]
    author: Mapped[str]
    price: Mapped[int]
    old_price: Mapped[int]
    quantity: Mapped[int]
    discount_amount: Mapped[int]

    order: Mapped["Order"] = relationship(back_populates="items")




