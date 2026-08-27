from database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "store_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    age: Mapped[int]
    login:Mapped[str]=mapped_column(unique=True)
    password_hash: Mapped[str]
    email: Mapped[str|None] = mapped_column(default=None)

    contact_number:Mapped[str|None]=mapped_column(default=None)

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")