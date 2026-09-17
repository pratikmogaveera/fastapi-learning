import json
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel

RATE_LIMITING_THRESHOLD = 5


@asynccontextmanager
async def lifespan(app: FastAPI):
  r = redis.Redis(decode_responses=True)
  app.state.redis = r
  yield
  await r.close()


app = FastAPI(lifespan=lifespan)


async def get_redis():
  return app.state.redis


async def rate_limiting_dep(request: Request, r: redis.Redis = Depends(get_redis)):
  client_ip = request.client.host  # type: ignore
  # Check client's hit count in cache
  current_hits = await r.incr(f"rate_limit:{client_ip}")

  if current_hits == 1:
    # First hit in atleast last 10s
    # Set expiry of 10s on cache key
    await r.expire(name=f"rate_limit:{client_ip}", time=10)
  elif current_hits > RATE_LIMITING_THRESHOLD:
    raise HTTPException(429, "You have reached the limit of requests.")

  return {"success": True}


class User(BaseModel):
  user_id: str
  name: str


users_table: list[User] = [
  User(user_id="1", name="Joey"),
  User(user_id="2", name="Joe"),
  User(user_id="3", name="Sam"),
  User(user_id="4", name="Tim"),
  User(user_id="5", name="Ben"),
]


@app.get("/users/{user_id}", response_model=User)
async def get_user_by_user_id(
  user_id: str, r: redis.Redis = Depends(get_redis), rate_limiting=Depends(rate_limiting_dep)
):
  # Check redis if user details exist in cache
  user_from_cache = await r.get(name=f"user:{user_id}")

  if user_from_cache is None:
    # If user not in cache, check db
    user_details = next((user for user in users_table if user.user_id == user_id), None)
    if user_details is None:
      # If user not in db, return error
      raise HTTPException(404, "User doesnt exist.")

    # User found in db, return
    # Set user details in cache with ttl of 60s
    json_as_string = json.dumps({"user_id": user_details.user_id, "name": user_details.name})
    await r.setex(name=f"user:{user_id}", time=60, value=json_as_string)
    return user_details

  # User found in cache, return
  return json.loads(user_from_cache)


@app.get("/limited")
async def rate_limiting(rate_limiting=Depends(rate_limiting_dep)):
  return {"success": True}
