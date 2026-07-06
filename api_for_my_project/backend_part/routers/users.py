from typing import Annotated

from fastapi import HTTPException, APIRouter, Body
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from argon2 import PasswordHasher
from database import engine, Base
from dependencies import get_session, get_authenticated_user
from models import User
from schemas import CreateUser, UserResponse

router = APIRouter()

@router.post("/users",response_model=UserResponse)
async def create_user(
        data: Annotated[CreateUser, Body()],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    ph = PasswordHasher()
    password_hash = ph.hash(data.password)

    stmt = select(User).where(User.login==data.login)
    existing_login = await session.scalar(stmt)
    if existing_login:
        raise HTTPException(
            status_code=400,
            detail="Данный логин уже занят другим пользователем"
        )

    new_user = User(
        login=data.login,
        password_hash= password_hash,
        name = data.name,
        age = data.age,
    )
    session.add(new_user)
    await session.commit()

    response = UserResponse(
        id=new_user.id,
        login=new_user.login,
        name=new_user.name,
        age=new_user.age)
    
    return response

@router.get("/users/me", response_model=UserResponse)
async def get_current_user(
        user: Annotated[User, Depends(get_authenticated_user)],
):
    response = UserResponse(
        id = user.id,
        login=user.login,
        name=user.name,
        age = user.age
    )
    return response



