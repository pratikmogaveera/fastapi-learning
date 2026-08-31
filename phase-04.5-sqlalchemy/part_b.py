from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

pg_engine = create_engine("postgresql://root:root@localhost:5432/fastapi-pg", echo=True)

# Core Method
metadata_obj = MetaData()

user_accounts = Table(
  "user_accounts",
  metadata_obj,
  Column("id", Integer, primary_key=True, autoincrement=True),
  Column("name", String(30), nullable=False),
  Column("fullname", String, nullable=False),
)

address = Table(
  "address",
  metadata_obj,
  Column("id", Integer, primary_key=True, autoincrement=True),
  Column("country", String, nullable=False),
  Column("state", String, nullable=False),
  Column("city", String, nullable=False),
  Column("user_id", Integer, ForeignKey("user_accounts.id"), nullable=False),
)


metadata_obj.create_all(pg_engine)

print(user_accounts.c.keys())
print(user_accounts.primary_key)


# ORM Method
class Base(DeclarativeBase):
  pass


class UserAccount(Base):
  __tablename__ = "users_table"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(30))
  fullname: Mapped[str]


class Address(Base):
  __tablename__ = "address_table"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  country: Mapped[str]
  state: Mapped[str]
  city: Mapped[str]
  user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))


Base.metadata.create_all(pg_engine)
