from sqlalchemy import select
from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uvicorn import run
from pydantic import BaseModel


app = FastAPI()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str]
    age: Mapped[int]
    password: Mapped[str]

class CreateUser(BaseModel):
    name: str
    age: int
    password: str

db_url = "postgresql+asyncpg://postgres:142536@127.0.0.1/postgres"
engine = create_async_engine(db_url, echo = True)

@app.post("/create-all")
async def create_all():
    conn = await engine.connect()
    await  conn.run_sync(Base.metadata.create_all)
    await conn.commit()
    await conn.close()


@app.post("/users")
async def create_user(payload:CreateUser):
    conn = await engine.connect()
    session = AsyncSession(conn)
    new_user = User(
        name = payload.name,
        age = payload.age,
        password = payload.password
    )
    session.add(new_user)
    await session.flush()

    result = {
        "id": new_user.id,
        "name": payload.name,
        "password": payload.password
    }

    await session.commit()
    await session.close()

    return result




@app.get("/users")
async def get_all_users():
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all() # возврат без кортежей
    await conn.close()

    return [
        {"id": user.id, "name": user.name, "age": user.age}
        for user in users
    ]



@app.get("/users/{user_id}")
async def get_user_by_id(user_id:int):
    conn = await engine.connect()
    session = AsyncSession(conn)

    stmt = (select(User)
            .where (User.id == user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        await conn.close()
        raise HTTPException(status_code=404)


    result_data = { "id": user.id,
               "age": user.age,
               "name": user.name
    }
    await conn.close()

    return result_data



@app.delete("/users/{user_id}")
async def delete_user_by_id(user_id:int):
    conn = await engine.connect()
    session = AsyncSession(conn)

    result = await session.execute(
        select(User).where(User.id==user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404)

    deleted_user= {
        "id": user.id,
        "name": user.name,
        "age": user.age
    }

    await session.delete(user)
    await session.commit()
    await session.close()

    return {
        "message": f"User with id {user_id} was deleted",
        "deleted_user": deleted_user
    }

run(app)

