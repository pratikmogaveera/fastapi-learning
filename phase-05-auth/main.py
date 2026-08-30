from datetime import datetime, timedelta, timezone
from typing import Annotated

from database import get_db
from fastapi import Depends, FastAPI, Header, HTTPException
from jose import JWTError, jwt
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Phase 5 — Authentication (JWT)
# Complete Phase 1–4 first, then come back here.
# See PLAN.md Phase 5 for tasks.


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


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


class Token(BaseModel):
  sub: str
  exp: datetime


class LoginUserRequest(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8, max_length=30)


class LoginUserResponse(BaseModel):
  message: str
  access_token: str
  user: UserResponse


def hash_password(raw_password: str) -> str:
  hashed_password = pwd_context.hash(raw_password)
  return hashed_password


def check_password(hashed_password: str, raw_password: str) -> bool:
  is_correct = pwd_context.verify(raw_password, hashed_password)
  return is_correct


def authenticate_jwt(authorization: str = Header(...)) -> str:
  print("Pratik", authorization)
  try:
    payload = jwt.decode(
      token=authorization.removeprefix("Bearer "), key="secret-key", algorithms=["HS256"]
    )
    token_data = Token(**payload)
    user_id = token_data.sub
    return user_id
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid session.")


@app.post("/create-user", response_model=UserResponse)
async def create_user(payload: CreaterUserRequest, session: AsyncSession = Depends(get_db)):
  new_user = Users(name=payload.name, email=payload.email, password=hash_password(payload.password))
  session.add(new_user)

  await session.commit()
  await session.refresh(new_user)

  return new_user


@app.post("/login", response_model=LoginUserResponse)
async def login_user(payload: LoginUserRequest, session: AsyncSession = Depends(get_db)):
  query = select(Users).where(Users.email == payload.email)
  result = await session.execute(query)
  user = result.scalar_one_or_none()

  if user is None:
    raise HTTPException(status_code=401, detail="Please enter correct credentials.")

  is_authenticated = check_password(hashed_password=user.password, raw_password=payload.password)
  if not is_authenticated:
    raise HTTPException(status_code=401, detail="Please enter correct credentials.")

  token_payload = {
    "sub": str(user.id),
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
  }

  token = jwt.encode(token_payload, key="secret-key", algorithm="HS256")

  return {"message": "Login Successful", "access_token": token, "user": user}


CurrentUser = Annotated[str, Depends(authenticate_jwt)]


@app.get("/me")
async def get_current_user(user_id: CurrentUser, session=Depends(get_db)) -> UserResponse:
  query = select(Users).where(Users.id == int(user_id))
  result = await session.execute(query)
  user = result.scalar_one_or_none()

  if user is None:
    raise HTTPException(status_code=401, detail="Something went wrong while fetching user details.")
  return user
