import asyncpg

from uvicorn import run
from fastapi import FastAPI
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
    name varchar not null
    )
    """)

class CreateUser(BaseModel):
    name: str


@app.post("/users")
async def create_user(payload:CreateUser):
    conn = await create_connection()
    try:
        await create_users_table(conn)

        row = await  conn.fetchrow("""
            insert into users(name) values ($1)
            returning id 
        """,payload.name)
        user_id = row["id"]

        return {
            "id": user_id,
            "name": payload.name
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




if __name__ == '__main__':
    run(app)








