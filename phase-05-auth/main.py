from datetime import datetime

from database import get_db
from fastapi import Depends, FastAPI
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_password: str) -> str:
    hashed_password = pwd_context.hash(raw_password)
    return hashed_password


def check_password(hashed_password: str, raw_password: str) -> bool:
    is_correct = pwd_context.verify(raw_password, hashed_password)
    return is_correct


app = FastAPI()

# Phase 5 — Authentication (JWT)
# Complete Phase 1–4 first, then come back here.
# See PLAN.md Phase 5 for tasks.


class CreaterUserRequest(BaseModel):
    name: str = Field(min_length=3, max_length=40, pattern=r"^[A-Za-z\s]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime


@app.post("/create-user", response_model=UserResponse)
async def create_user(payload: CreaterUserRequest, session: AsyncSession = Depends(get_db)):
    new_user = Users(
        name=payload.name, email=payload.email, password=hash_password(payload.password)
    )
    session.add(new_user)

    await session.commit()
    await session.refresh(new_user)

    return new_user
