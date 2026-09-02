from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from database import engine, Base
from routers import (
    books_router,
    cart_router,
    favorites_router,
    orders_router,
    users_router,
)
from sessions import router as sessions_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await  engine.dispose()

app = FastAPI(
    title = "Book Store API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
           "http://localhost:5173",
           "http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router,tags=["books"])
app.include_router(cart_router, tags=["cart"])
app.include_router(favorites_router,tags=["favorites"])
app.include_router(users_router,tags=["users"])
app.include_router(orders_router, tags=["orders"])
app.include_router(sessions_router, tags=["sessions"])



if __name__ == '__main__':
    run(app)



