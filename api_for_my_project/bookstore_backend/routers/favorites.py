from typing import Annotated
from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from dependencies import get_session, get_authenticated_user
from database import engine
from models import Favorite, Book, User
from schemas import FavoriteResponse

router = APIRouter()

def build_fav_response(fav_item):
    return FavoriteResponse(
        id = fav_item.id,
        book_id=fav_item.book_id,
        title= fav_item.book.title,
        author=fav_item.book.author,
        price=fav_item.book.price,
        old_price=fav_item.book.old_price,
        image=fav_item.book.image,
    )

@router.post("/favorites/{book_id}")
async def add_to_favorites(
        book_id:int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):
    stmt = select(Favorite).where(
        Favorite.user_id == user.id,
        Favorite.book_id == book_id
    )
    result = await session.execute(stmt)
    is_in_fav = result.scalar_one_or_none()

    if is_in_fav:
        raise HTTPException(status_code=400, detail = 'Книга уже есть в избранном')

    stmt = select(Book).where(Book.id==book_id)
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code = 404,detail = "Книга не найдена")

    new_favorite = Favorite(
        user_id= user.id,
        book_id = book_id,
    )
    session.add(new_favorite)
    await session.flush()

    stmt = (
        select(Favorite)
        .options(joinedload(Favorite.book))
        .where (Favorite.id == new_favorite.id)
    )
    result = await session.execute(stmt)
    favorite_with_book= result.scalar_one()
    await session.commit()


    response = build_fav_response(favorite_with_book)
    return response


@router.get("/favorites")
async def get_favorites(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):

    stmt = (
        select(Favorite)
        .options(joinedload(Favorite.book))
        .where(Favorite.user_id == user.id)
    )
    result = await session.execute(stmt)
    items = result.scalars().all()

    response = [build_fav_response(item) for item in items]

    return response


@router.delete("/favorites/{book_id}")
async def delete_from_favorites(
        book_id:int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):

    stmt = select (Favorite).where (
        Favorite.user_id == user.id,
        Favorite.book_id == book_id
                   )
    result = await session.execute(stmt)
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(status_code = 404, detail = "Книги нет в избранном")

    await session.delete(favorite)
    await session.commit()

    return {
        "message": "Удалено из избранного"
    }


@router.delete("/favorites")
async def clear_all_favorites(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):
    stmt = select(Favorite).where(Favorite.user_id == user.id)
    result = await session.execute(stmt)
    items = result.scalars().all()

    if not items:
        return {"message": "В избранном нет книг"}

    for item in items:
        await session.delete(item)

    await session.commit()
    return {
        "message": "Избранное очищено"
    }









