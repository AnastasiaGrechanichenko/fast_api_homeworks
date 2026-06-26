
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import engine, Base
from models import CartItem, Book,User
from schemas import CreateCartItem, CartItemResponse, CartResponse, UpdateCartRequest, CreateUser, CreateBook, \
    BookResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/create-all_tables")
async def create_all_tables():
    conn =  await engine.connect()
    await conn.run_sync(Base.metadata.create_all)
    await conn.commit()
    await conn.close()
    return {"message": "Таблицы созданы"}


@app.post("/users")
async def create_user(data:CreateUser):
    conn = await engine.connect()
    session = AsyncSession(conn)

    new_user = User(
        name = data.name,
        age = data.age,
        password = data.password,
    )

    session.add(new_user)
    await session.flush()

    response = {
        "id" : new_user.id,
        "name": data.name,
        "age": data.age,
    }
    await session.commit()
    await conn.close()
    return response

@app.post("/books")
async def create_book(data: CreateBook):
    conn = await engine.connect()
    session = AsyncSession(conn)

    new_book = Book(
        title = data.title,
        author= data.author,
        price=data.price,
        old_price=data.old_price,
        image=data.image,
        category=data.category
    )
    session.add(new_book)
    await session.flush()
    await session.refresh(new_book)
    response = BookResponse(
        id = new_book.id,
        title=new_book.title,
        author=new_book.author,
        price=new_book.price,
        old_price=new_book.old_price,
        image=new_book.image,
        category=new_book.category,
    )
    await session.commit()
    await conn.close()
    return response

@app.get("/books")
async def get_all_books():
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = select(Book)
    result = await session.execute(stmt)
    books = result.scalars().all()

    response = []
    for book in books:
        response.append(BookResponse(
            id = book.id,
            title = book.title,
            author = book.author,
            price = book.price,
            old_price = book.old_price,
            image = book.image,
            category=book.category,
        ))
    await conn.close()
    return response


@app.get("/books/{book_id}")
async def get_book_by_id(book_id:int):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = select(Book).where(Book.id == book_id)
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    response = BookResponse(
        id=book.id,
        title=book.title,
        author=book.author,
        price=book.price,
        old_price=book.old_price,
        image=book.image,
        category=book.category,
    )

    await conn.close()
    return response






@app.post("/users/{user_id}/cart")
async def add_book_to_cart(user_id:int, data: CreateCartItem):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = (
        select(CartItem).where(CartItem.user_id == user_id,
                                  CartItem.book_id == data.book_id)
    )
    result = await session.execute(stmt)
    is_in_db = result.scalar_one_or_none()

    if is_in_db:
        is_in_db.quantity += data.quantity
        await session.flush()
        await session.refresh(is_in_db)

        response = CartItemResponse(
            id = is_in_db.id,
            book_id = is_in_db.book_id,
            title = is_in_db.book.title,
            author = is_in_db.book.author,
            price =is_in_db.book.price,
            old_price=is_in_db.book.old_price,
            quantity = is_in_db.quantity
        )
        await session.commit()
        await conn.close()
        return response
    stmt = select (Book).where (Book.id== data.book_id)
    result = await session.execute(stmt)
    book = result.scalar_one_or_none()

    if not book:
        await conn.close()
        raise HTTPException(status_code=404, detail="Книга не найдена")

    new_cart_item = CartItem(
        user_id = user_id,
        book_id = data.book_id,
        quantity = data.quantity)
    session.add(new_cart_item)
    await session.flush()
    await session.refresh(new_cart_item)

    response = CartItemResponse(
        id = new_cart_item.id,
        book_id = new_cart_item.book_id,
        title = book.title,
        author = book.author,
        price = book.price,
        old_price=book.old_price,
        quantity=new_cart_item.quantity
    )
    await session.commit()
    await conn.close()
    return response



@app.get("/users/{user_id}/cart")
async def get_user_cart(user_id:int):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = (select(CartItem)
    .options(joinedload(CartItem.book))
    .where(CartItem.user_id == user_id)
           )
    result = await session.execute(stmt)
    items = result.scalars().all()

    response_items = []
    for item in items:
        response_items.append(CartItemResponse(
            id = item.id,
            book_id= item.book_id,
            title = item.book.title,
            author = item.book.author,
            price = item.book.price,
            old_price=item.book.old_price,
            quantity=item.quantity,
        ))
    await conn.close()
    return CartResponse(items=response_items)

@app.patch("/users/{user_id}/cart/{item_id}")
async def update_quantity(user_id: int, item_id:int, data:UpdateCartRequest):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = (select(CartItem)
            .options(joinedload(CartItem.book))
            .where(CartItem.id == item_id, CartItem.user_id== user_id))
    result = await session.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        await conn.close()
        raise HTTPException(status_code=404, detail="Книга не найдена")

    cart_item.quantity = data.quantity
    await session.flush()
    response = CartItemResponse(
        id=cart_item.id,
        book_id=cart_item.book_id,
        title=cart_item.book.title,
        author=cart_item.book.author,
        price=cart_item.book.price,
        old_price=cart_item.book.old_price,
        quantity=cart_item.quantity,
    )
    await session.commit()
    await conn.close()
    return response


@app.delete("/users/{user_id}/cart/{item_id}")
async def delete_item_from_cart(user_id:int, item_id:int):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = (select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id))
    result = await session.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        await conn.close()
        raise HTTPException(status_code=404, detail="Книга не найдена")


    await session.delete(cart_item)
    await session.commit()
    await conn.close()

    return {"message":"Книга удалена из корзины"}



@app.delete("/users/{user_id}/cart")
async def clear_cart(user_id:int):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = (select(CartItem).where(CartItem.user_id==user_id))
    result = await session.execute(stmt)
    items = result.scalars().all()

    if not items:
        await conn.close()
        return {"message":"Корзина уже пуста"}

    for item in items:
        await session.delete(item)

    await session.commit()
    await conn.close()
    return {"message":"Корзина очищена"}

run(app)
