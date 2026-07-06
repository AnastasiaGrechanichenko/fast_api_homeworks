from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from database import Base


class LoginSession(Base):
    __tablename__="login_sessions"

    id: Mapped[int] = mapped_column(primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey("store_users.id"))
    secret: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)