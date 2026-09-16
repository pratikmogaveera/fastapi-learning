import asyncio

import redis.asyncio as redis


async def main():
  async with redis.Redis(host="localhost", port=6379, decode_responses=True) as r:
    # Task 1: Set and Get value
    await r.set(name="name", value="Pratik")
    value = await r.get(name="name")
    print(f"name: {value}")

    # Task 2: Delete the previous set value
    await r.delete("name")

    # Task 3: Check if the key still exists
    name_exists = await r.exists("name")
    print("Yes" if name_exists == 1 else "No")

    # Task 4: Set an expiring key 'session' with 5s expiry and track its value
    await r.setex(name="session", time=5, value="abc123")
    value = await r.get(name="session")
    print(f"Value before 5s expiry: {value}")

    await asyncio.sleep(6)
    value = await r.get(name="session")
    print(f"Value after 5s expiry: {value}")

    # Task 5: Set expiry after setting value, and check its TTL
    await r.set(name="temp", value="test")
    await r.expire(name="temp", time=10)
    await asyncio.sleep(3)
    pending_ttl = await r.ttl(name="temp")
    print(f"TTL after 3s: {pending_ttl}")

    # Task 6: INCR 'visits' thrice and check value
    count = await r.incr(name="visits")
    print(f"'visits' count: {count}")
    count = await r.incr(name="visits")
    print(f"'visits' count: {count}")
    count = await r.incr(name="visits")
    print(f"'visits' count: {count}")

    # Task 7: Print all keys present
    print(f"All keys: {await r.keys(pattern='*')}")


asyncio.run(main())
