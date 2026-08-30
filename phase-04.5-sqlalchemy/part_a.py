from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
pg_engine = create_engine("postgresql://root:root@localhost:5432/fastapi-pg", echo=True)


with engine.connect() as conn:
  print("Checking connection:")
  result = conn.execute(text("SELECT 1"))
  print(result.all())


with engine.connect() as conn:
  print("Checking DDL and DML operations [.connect()]:")
  conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x int NULL,y varchar NULL);"))
  conn.commit()

  conn.execute(text("INSERT INTO some_table (x, y) VALUES(:x, :y)"), [{"x": 1, "y": "hello"}])
  conn.commit()

  result = conn.execute(text("SELECT * FROM some_table"))
  print(result.all())


with engine.begin() as conn:
  print("Checking DDL and DML operations [.begin()]:")
  conn.execute(text("INSERT INTO some_table (x, y) VALUES(:x, :y)"), [{"x": 2, "y": "message"}])

  result = conn.execute(text("SELECT * FROM some_table"))
  print(result.all())


with pg_engine.begin() as conn:
  print("Checking DDL and DML operations in PG Database [.begin()]:")
  conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x int NULL,y varchar NULL);"))

  conn.execute(
    text("INSERT INTO some_table (x, y) VALUES(:x, :y)"),
    [{"x": 1, "y": "one"}, {"x": 2, "y": "two"}],
  )

  result = conn.execute(text("SELECT * FROM some_table"))
  print(result.all())
