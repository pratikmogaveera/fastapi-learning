import asyncio

from arq import create_pool
from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings()


async def main():
  redis = await create_pool(REDIS_SETTINGS)
  await redis.enqueue_job("test_retry", "email@domain.com")
  await redis.enqueue_job("test_timeout", _defer_by=15)
  await redis.enqueue_job("test_unique_jobid_dedupe", _defer_by=20, _job_id="unique-job-id")
  await redis.enqueue_job("test_unique_jobid_dedupe", _defer_by=20, _job_id="unique-job-id")


asyncio.run(main())
