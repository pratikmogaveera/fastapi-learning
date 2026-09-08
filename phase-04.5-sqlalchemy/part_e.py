import asyncio

from part_b import UserAccount
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

pg_engine = create_async_engine(
  "postgresql+asyncpg://root:root@localhost:5432/fastapi-pg", echo=True
)

SessionFactory = async_sessionmaker(bind=pg_engine, class_=AsyncSession, expire_on_commit=False)


async def main():
  async with SessionFactory() as session:
    new_user = UserAccount(name="Pratik", fullname="Pratik Mogaveera")
    print(new_user.id, new_user.name, new_user.fullname)
    session.add(new_user)
    await session.flush()
    print(new_user.id, new_user.name, new_user.fullname)
    await session.commit()

    user = await session.get(UserAccount, new_user.id)
    assert user is not None
    latest_user_id = user.id
    print(user is new_user)
    print(user.id, user.name, user.fullname)
    user.name = "Rushil"

    await session.commit()

    user = await session.get(UserAccount, latest_user_id)
    assert user is not None

    print(user.id, user.name, user.fullname)

    user.fullname = "Changed Name"
    print(user.fullname)
    await session.rollback()

    await session.get(UserAccount, latest_user_id)
    print(user.fullname)

    await session.delete(user)
    await session.commit()


asyncio.run(main())
