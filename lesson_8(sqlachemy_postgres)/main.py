from contextlib import asynccontextmanager


from fastapi import FastAPI,HTTPException
from uvicorn import run
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Запуск приложения")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы")
    yield

    print("Приложение останавливается")


    await engine.dispose()


app = FastAPI(lifespan=lifespan)

db_url = "postgresql+asyncpg://postgres:142536@127.0.0.1/postgres"
engine = create_async_engine(db_url, echo = True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users01"
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str]
    age : Mapped[int]

class CreateUser(BaseModel):
    name: str
    age: int


@app.post("/users")
async def create_user(payload:CreateUser):
    async with AsyncSessionLocal() as session:
        new_user =User(name = payload.name, age = payload.age)

        session.add(new_user)

        await session.commit()

        await session.refresh(new_user)

        return {"id": new_user.id,
                "name": new_user.name,
                "age": new_user.age
        }

@app.get("/users")
async def get_all_users():
    async with AsyncSessionLocal() as session:

        result = await session.execute(select(User))

        users  = result.scalars().all()

        return [{"id": user.id, "name": user.name, "age": user.age} for user in users ]


@app.get("/users/{user_id}")
async def get_user_by_id(user_id:int):
    async  with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.id ==user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return {"message" :f"Пользователь с id {user_id} не найден"}
        return {"id": user.id,
                "name": user.name,
                "age": user.age
                }



@app.put("/users/{user_id}")
async def update_user(user_id:int, payload:CreateUser):

    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_or_none()

        if not user:
            raise  HTTPException (
                status_code = 404,
                detail = f" Пользователь с {user_id} не найден "
            )
        user.name = payload.name
        user.age = payload.age

        await session.commit()
        return { "id": user.id,
                 "name": user.name,
                 "age": user.age,
                 "message" : f"Пользователь с {user_id} успешно обновлен"

        }
@app.delete("/users/{user_id}")
async def delete_user(user_id:int):
    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(User).where(User.id==user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException (
                status_code = 404,
                detail = f"Пользователь с {user_id} не найден "
            )
        deleted_user = {
            "id": user.id,
            "name":user.name,
            "age": user.age
        }

        await session.delete(user)

        await session.commit()

        return {"message" :  f"Пользователь с {user_id} успешно удален" }



run(app)
