
from typing import Annotated
from uuid import uuid4

from argon2 import PasswordHasher
from fastapi import APIRouter, Header, Depends,HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session
from models import User, LoginSession
from schemas.user import LogineSessionResponse

router = APIRouter()


@router.post("/sessions", response_model=LogineSessionResponse)
async def create_session(
        login: Annotated[str, Header()],
        password: Annotated[str,Header()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    ph = PasswordHasher()

    stmt = select(User).where(User.login == login)
    user = await session.scalar(stmt)

    if user is None:
        dummy_hash = ("$argon2id$v=19$m=65536,t=3,p=4$1/kKopFhFTmJP0aLfW"
                      "15XQ$fwP4HIJ1Dwtk7Fb5XzW8HDenJ7WroA6fiz0FAynO1cA")
        dummy_password = "dummy pointless password sky earth"
        ph.verify(dummy_hash, dummy_password)
        raise HTTPException(
            status_code = 401,
            detail = "Не аутентифицирован"
        )

    try:
        ph.verify(user.password_hash, password)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Не аутентифицирован"
        )

    new_login_session = LoginSession(
        user_id = user.id,
        secret = str(uuid4()),
    )
    session.add(new_login_session)
    await session.commit()

    return LogineSessionResponse(
        user_id= new_login_session.user_id,
        secret=new_login_session.secret,
    )


