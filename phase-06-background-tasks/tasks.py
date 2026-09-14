import asyncio

from utils.helper import ts


async def send_welcome_email(ctx, email: str):
  await asyncio.sleep(3)
  print(f"[{ts()}] Welcome email sent successfully to {email}")
