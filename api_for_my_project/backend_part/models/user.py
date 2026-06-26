from database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "store_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    age: Mapped[int]
    password: Mapped[str]

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")