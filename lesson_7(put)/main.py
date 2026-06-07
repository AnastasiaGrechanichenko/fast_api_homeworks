import asyncpg

from uvicorn import run
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


async def create_connection():
    conn = await  asyncpg.connect(
        "postgresql://postgres:142536@127.0.0.1/postgres"
    )
    return conn

async def create_users_table(conn):
    await conn.execute("""
    create table if not exists users (
    id integer generated always as identity primary key,
    name varchar not null,
    age integer not null
    )
    """)

class CreateUser(BaseModel):
    name: str
    age: int


@app.post("/users")
async def create_user(payload:CreateUser):
    conn = await create_connection()
    try:
        await create_users_table(conn)

        row = await  conn.fetchrow("""
            insert into users(name,age) values ($1, $2)
            returning id 
        """,payload.name, payload.age)
        user_id = row["id"]

        return {
            "id": user_id,
            "name": payload.name,
            "age": payload.age
        }
    finally:
        await  conn.close()


@app.get("/users")
async def get_users():
    conn = await  create_connection()
    await create_users_table(conn)

    data = await conn.fetch("""
    select * from users 
    """)
    await  conn.close()
    return data

@app.put("/users/{user_id}")
async def update_user(user_id: int, payload: CreateUser):
    conn = await create_connection()
    try:
        await create_users_table(conn)

        existing_user = await conn.fetchrow("""
        select  id from users where id = $1
        """, user_id)

        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail=f" User with id {user_id} doesn't exist "
            )
        await  conn.execute("""
        update users 
        set name = $1, age = $2
        where id = $3
        """, payload.name, payload.age, user_id)
        return {
            "id": user_id,
            "name": payload.name,
            "age": payload.age
        }
    finally:
        await conn.close()






if __name__ == '__main__':
    run(app)







