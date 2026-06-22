from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

db_url = "postgresql+asyncpg://postgres:142536@127.0.0.1/postgres"
engine = create_async_engine(db_url,echo = True)
AsyncSessionLocal = async_sessionmaker(engine,expire_on_commit=False)
class Base(DeclarativeBase):
    pass
