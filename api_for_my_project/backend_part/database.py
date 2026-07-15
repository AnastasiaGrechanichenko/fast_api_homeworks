from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from models.user import User
from models.book import Book
from models.cart import CartItem
from models.favorite import Favorite
from models.order import Order, OrderItem
from models.login_session import LoginSession


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
db_url = "postgresql+asyncpg://postgres:142536@127.0.0.1/postgres"
engine = create_async_engine(db_url,echo = True)
AsyncSessionLocal = async_sessionmaker(engine,expire_on_commit=False)

