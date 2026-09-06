from part_b import address, user_accounts
from sqlalchemy import create_engine, delete, insert, select, update

pg_engine = create_engine("postgresql://root:root@localhost:5432/fastapi-pg", echo=False)

with pg_engine.connect() as conn:
  insert_user_stmt = (
    insert(user_accounts)
    .returning(user_accounts.c.id, user_accounts.c.name, user_accounts.c.fullname)
    .values(name="Pratik", fullname="Pratik Mogaveera")
  )
  result = conn.execute(insert_user_stmt)
  result_values = result.all()
  print(result_values)
  conn.commit()

  insert_address_stmt = (
    insert(address)
    .returning(address.c.country, address.c.state, address.c.city)
    .values(
      {
        "country": "India",
        "state": "Maharashtra",
        "city": "Mumbai",
        "user_id": result_values[0].id,
      },
    )
  )
  result = conn.execute(insert_address_stmt)
  print(result.all())
  conn.commit()

  select_all_stmt = select(user_accounts)
  result = conn.execute(select_all_stmt)
  print(result.all())

  multi_insert_stmt = (
    insert(user_accounts)
    .returning(user_accounts.c.id, user_accounts.c.name, user_accounts.c.fullname)
    .values(
      [
        {"name": "Rushil", "fullname": "Rushil Joshi"},
        {"name": "Shivam", "fullname": "Shivam Pancholi"},
      ]
    )
  )

  result = conn.execute(multi_insert_stmt)
  print(result.all())
  conn.commit()

  select_with_where_stmt = select(user_accounts).where(user_accounts.c.name == "Pratik")
  result = conn.execute(select_with_where_stmt)
  print(result.all())

  select_name_stmt = select(user_accounts.c.name)
  result = conn.execute(select_name_stmt)
  print(result.all())

  join_user_address_stmt = select(user_accounts.c.name, address.c.state).join(
    address, user_accounts.c.id == address.c.user_id
  )
  result = conn.execute(join_user_address_stmt)
  print(result.all())

  update_stmt = (
    update(user_accounts)
    .where(user_accounts.c.name == "Pratik")
    .values({"fullname": "Pratik Chandra Mogaveera"})
    .returning(user_accounts.c.fullname)
  )

  result = conn.execute(update_stmt)
  print(result.all())
  conn.commit()

  delete_stmt = (
    delete(user_accounts)
    .where(user_accounts.c.name == "Shivam")
    .returning(user_accounts.c.fullname)
  )

  result = conn.execute(delete_stmt)
  print(result.all())
  conn.commit()
