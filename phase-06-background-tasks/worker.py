from arq import func
from arq.connections import RedisSettings
from tasks import send_welcome_email

REDIS_SETTINGS = RedisSettings()


async def startup(ctx):
  print("[Worker] Server started.")


async def shutdown(ctx):
  print("[Worker] Server shutting down.")


class WorkerSettings:
  functions = [func(send_welcome_email, max_tries=3)]
  on_startup = startup
  on_shutdown = shutdown
  redis_settings = REDIS_SETTINGS
