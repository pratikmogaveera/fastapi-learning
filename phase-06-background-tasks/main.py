import asyncio

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from utils.helper import ts

app = FastAPI()

# Phase 6 — Background Tasks & Workers (ARQ)
# Complete Phase 1–5 first, then come back here.
# See PLAN.md Phase 6 for tasks.


async def send_welcome_email(email: str):
  await asyncio.sleep(3)
  print(f"[{ts()}] Welcome email send succesfully to {email}")


class RegisterUserPayload(BaseModel):
  email: str
  name: str


class RegisterUserResponse(BaseModel):
  success: bool
  message: str


@app.post("/register", response_model=RegisterUserResponse)
async def register_user(payload: RegisterUserPayload, background_tasks: BackgroundTasks):
  print(f"[{ts()}] Request received.")
  background_tasks.add_task(send_welcome_email, payload.email)
  return {"success": True, "message": "Congratulations! You have been registered successfully."}
