import asyncio

from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings()


async def startup(ctx):
  print("[Worker] Server started.")


async def shutdown(ctx):
  print("[Worker] Server shutting down.")


async def send_welcome_email(ctx, email: str):
  await asyncio.sleep(3)
  print(f"Welcome email sent to {email}")


class WorkerSettings:
  functions = [send_welcome_email]
  on_startup = startup
  on_shutdown = shutdown
  redis_settings = REDIS_SETTINGS
