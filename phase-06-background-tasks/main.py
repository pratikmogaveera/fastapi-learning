from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.helper import ts

REDIS_SETTINGS = RedisSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
  # startup
  print("Lifespan starting.")
  redis = await create_pool(REDIS_SETTINGS)
  app.state.arq_pool = redis
  yield

  # shutdown
  print("Lifespan ending.")
  await redis.close()


app = FastAPI(lifespan=lifespan)

# Phase 6 — Background Tasks & Workers (ARQ)


class RegisterUserPayload(BaseModel):
  email: str
  name: str


class RegisterUserResponse(BaseModel):
  success: bool
  message: str


@app.post("/register", response_model=RegisterUserResponse)
async def register_user(payload: RegisterUserPayload, request: Request):
  print(f"[{ts()}] Request received.")
  await request.app.state.arq_pool.enqueue_job("send_welcome_email", payload.email)
  return {"success": True, "message": "Congratulations! You have been registered successfully."}
