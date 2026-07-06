from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models import CartItem, Book, User
from schemas import CartItemResponse, CartResponse, CreateCartItem, UpdateCartRequest
from dependencies import get_session, get_authenticated_user


router = APIRouter()

def build_cart_response(item):
    return CartItemResponse(
        id = item.id,
        book_id=item.book_id,
        title=item.book.title,
        author=item.book.author,
        price=item.book.price,
        old_price=item.book.old_price,
        image=item.book.image,
        quantity=item.quantity,
    )

@router.post("/cart")
async def add_book_to_cart(
        data: CreateCartItem,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):

    stmt = (
        select(CartItem)
        .options(joinedload(CartItem.book))
        .where(
            CartItem.user_id == user.id,
            CartItem.book_id == data.book_id)
    )
    result = await session.execute(stmt)
    is_in_db = result.scalar_one_or_none()

    if is_in_db:
        is_in_db.quantity = data.quantity
        await session.commit()

        stmt= (
            select(CartItem)
            .options(joinedload(CartItem.book))
            .where(CartItem.id== is_in_db.id)
        )
        result = await session.execute(stmt)
        refreshed = result.scalar_one()

        response = build_cart_response(refreshed)
        return response
    stmt = select (Book).where (Book.id== data.book_id)
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    new_cart_item = CartItem(
        user_id = user.id,
        book_id = data.book_id,
        quantity = data.quantity
    )
    session.add(new_cart_item)
    await session.flush()

    stmt = (
        select(CartItem)
        .options(joinedload(CartItem.book))
        .where(CartItem.id == new_cart_item.id)
    )
    result = await session.execute(stmt)
    item_info =result.scalar_one()

    await session.commit()
    response = build_cart_response(item_info)
    return response


@router.get("/cart")
async def get_user_cart(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):
    stmt = (select(CartItem)
    .options(joinedload(CartItem.book))
    .where(CartItem.user_id == user.id)
           )
    result = await session.execute(stmt)
    items = result.scalars().all()

    response_items = [build_cart_response(item) for item in items]
    return CartResponse(items=response_items)

@router.patch("/cart/{item_id}")
async def update_quantity(
        item_id:int,
        data:UpdateCartRequest,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
        ):

    stmt = (select(CartItem)
            .options(joinedload(CartItem.book))
            .where(CartItem.id == item_id, CartItem.user_id== user.id))
    result = await session.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    cart_item.quantity = data.quantity
    await session.commit()

    response = build_cart_response(cart_item)
    return response


@router.delete("/cart/{item_id}")
async def delete_item_from_cart(
        item_id:int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):

    stmt = select(CartItem).where(
        CartItem.id == item_id,
        CartItem.user_id == user.id,
    )
    result = await session.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    await session.delete(cart_item)
    await session.commit()

    return {"message":"Книга удалена из корзины"}



@router.delete("/cart")
async def clear_cart(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):

    stmt = (select(CartItem).where(CartItem.user_id==user.id))
    result = await session.execute(stmt)
    items = result.scalars().all()

    if not items:
        return {"message":"Корзина уже пуста"}

    for item in items:
        await session.delete(item)

    await session.commit()
    return {"message":"Корзина очищена"}


