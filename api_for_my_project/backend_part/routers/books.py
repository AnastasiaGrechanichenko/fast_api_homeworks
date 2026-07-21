from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from dependencies import get_session
from models import Book
from schemas import BookResponse, CreateBook

router = APIRouter()

def build_book_response(book):
    return BookResponse(
        id = book.id,
        title = book.title,
        author = book.author,
        price=book.price,
        old_price=book.old_price,
        image=book.image,
        category=book.category,
        description = book.description,
    )

@router.post("/books")
async def create_book(
        data: CreateBook,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    new_book = Book(
        title = data.title,
        author= data.author,
        price=data.price,
        old_price=data.old_price,
        image=data.image,
        category=data.category
    )
    session.add(new_book)
    await session.commit()

    response = build_book_response(new_book)
    return response

@router.get("/books")
async def get_all_books(
        session: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = select(Book)
    result = await session.execute(stmt)
    books = result.scalars().all()

    response = [build_book_response(book)for book in books]

    return response


@router.get("/books/{book_id}")
async def get_book_by_id(
        book_id:int,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = select(Book).where(Book.id == book_id)
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    response = build_book_response(book)
    return response

