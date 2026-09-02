import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal,engine,Base
from models import Book
from data_seed import all_books

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        result= await session.execute(select(Book))
        if result.scalars().first():
            print('Данные уже есть, seed пропущен')
            return

        for book_data in all_books:
            book = Book(**book_data)
            session.add(book)

        await session.commit()
        print(f'Добавлено {len(all_books)} книг')

if __name__ == '__main__':
    asyncio.run(seed())

