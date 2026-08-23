from typing import Annotated
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from dependencies import get_session, get_authenticated_user
from models import CartItem, Order, OrderItem, User
from schemas import OrderItemResponse, OrderResponse,CreateOrderRequest

router = APIRouter()

def build_order_item_response(item):
    return OrderItemResponse(
        id = item.id,
        book_id = item.book_id,
        title = item.title,
        author = item.author,
        price = item.price,
        old_price = item.old_price,
        quantity = item.quantity,
        discount_amount = item.discount_amount
    )


def build_order_response(order):
    return OrderResponse(
        id = order.id,
        user_id = order.user_id,
        total_sum = order.total_sum,
        total_discount = order.total_discount,
        status = order.status,
        created_at = order.created_at,
        items = [build_order_item_response(item) for item in order.items],
    )

@router.post("/orders")
async def create_user_order(
        body:CreateOrderRequest,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User,Depends(get_authenticated_user)],
        ):
    stmt = (
        select(CartItem)
        .options(joinedload(CartItem.book))
        .where(CartItem.user_id==user.id)
    )
    result = await session.execute(stmt)
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(
            status_code = 400,
            detail = "Корзина пуста"
        )
    total = 0
    total_discount = 0

    for item in cart_items:
        total+=item.book.price*item.quantity
        total_discount +=(item.book.old_price - item.book.price)*item.quantity

    new_order = Order(
        user_id  = user.id,
        total_sum = total,
        total_discount = total_discount,
        status="pending",
        created_at = datetime.now(),
        recipient_name=body.recipient_name,
        phone=body.phone,
        address=body.address,
        payment_status=body.payment_status
    )
    session.add(new_order)
    await session.flush()

    for item in cart_items:
        order_item = OrderItem (
            order_id = new_order.id,
            book_id = item.book_id,
            title = item.book.title,
            author=item.book.author,
            price=item.book.price,
            old_price=item.book.old_price,
            quantity=item.quantity,
            discount_amount = (item.book.old_price - item.book.price) * item.quantity,
        )
        session.add(order_item)
    await session.execute(delete(CartItem)
                          .where(CartItem.user_id==user.id))
    await session.commit()

    stmt = (
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.id == new_order.id)
    )
    result = await session.execute(stmt)
    order_with_items = result.unique().scalar_one()
    return build_order_response(order_with_items)


@router.get("/orders")
async def get_user_orders (
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User,Depends(get_authenticated_user)],
):

    stmt = (
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.user_id==user.id)
            )
    result = await session.execute(stmt)
    orders = result.unique().scalars().all()

    response = [build_order_response(order) for order in orders]
    return response

@router.get("/orders/{order_id}")
async def get_order(
        order_id:int,
        session: Annotated[AsyncSession, Depends(get_session)],
        user: Annotated[User,Depends(get_authenticated_user)],
):
    stmt = (
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.id == order_id, Order.user_id==user.id)
    )
    result = await session.execute(stmt)
    order = result.unique().scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден ")

    return build_order_response(order)


@router.patch("/orders/{order_id}/cancel")
async def cancel_order(
        order_id:int,
        session: Annotated[AsyncSession,Depends(get_session)],
        user: Annotated[User, Depends(get_authenticated_user)],
):


    stmt = select(Order).where(Order.id == order_id, Order.user_id == user.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    if order.status =="cancelled":
        raise HTTPException(status_code=400, detail = "Заказ уже был отменен")

    if order.status in ("shipped", "delivered"):
        raise HTTPException(status_code=400, detail="Заказ не может быть отменен")
    order.status = "cancelled"
    await session.commit()

    stmt = (
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.id == order_id)
    )
    result = await session.execute(stmt)
    order_with_items = result.unique().scalar_one()

    return build_order_response(order_with_items)











