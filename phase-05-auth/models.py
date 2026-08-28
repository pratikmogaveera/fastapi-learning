from datetime import datetime

from database import Base
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
