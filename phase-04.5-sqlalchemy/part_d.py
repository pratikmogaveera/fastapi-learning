from part_b import UserAccount
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

pg_engine = create_engine("postgresql://root:root@localhost:5432/fastapi-pg", echo=True)

SessionFactory = sessionmaker(bind=pg_engine, expire_on_commit=False)


with Session(pg_engine) as session:
  new_user = UserAccount(name="Pratik", fullname="Pratik Mogaveera")
  print(new_user.id, new_user.name, new_user.fullname)
  session.add(new_user)
  session.flush()
  print(new_user.id, new_user.name, new_user.fullname)
  session.commit()

  user = session.get(UserAccount, new_user.id)
  assert user is not None
  latest_user_id = user.id
  print(user is new_user)
  print(user.id, user.name, user.fullname)
  user.name = "Rushil"

  session.commit()

with SessionFactory() as session:
  user = session.get(UserAccount, latest_user_id)
  assert user is not None

  print(user.id, user.name, user.fullname)

  user.fullname = "Changed Name"
  print(user.fullname)
  session.rollback()
  print(user.fullname)

  session.delete(user)
  session.commit()
