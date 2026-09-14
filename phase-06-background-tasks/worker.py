import asyncio

from arq import Retry, func
from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings()


async def startup(ctx):
  print("[Worker] Server started.")


async def shutdown(ctx):
  print("[Worker] Server shutting down.")


async def test_retry(ctx, email: str):
  await asyncio.sleep(3)
  raise Retry()


async def test_timeout(ctx):
  await asyncio.sleep(5)
  print("This job should never run.")


async def test_unique_jobid_dedupe(ctx):
  print("This job should run only once.")


class WorkerSettings:
  functions = [
    func(test_retry, max_tries=3),
    func(test_timeout, timeout=3, max_tries=1),
    func(test_unique_jobid_dedupe),
  ]
  on_startup = startup
  on_shutdown = shutdown
  redis_settings = REDIS_SETTINGS
