import asyncio

from arq import create_pool
from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings()


async def main():
  redis = await create_pool(REDIS_SETTINGS)
  await redis.enqueue_job("send_welcome_email", "pratik@test.com")


asyncio.run(main())
