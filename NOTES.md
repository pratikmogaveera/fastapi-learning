# FastAPI Learning — Notes

Concepts, Q&A, and key takeaways. Append after completing each phase. Don't reorganize.

---

## 1. Routing & Request Handling

### Key Concepts

- Route decorators (`@app.get`, `@app.post`, etc.) register a function as a handler for that HTTP method + path.
- Path parameters are declared in the path string as `{name}` and in the function signature as a typed argument — FastAPI validates and coerces the type automatically. Invalid types return a 422.
- Query parameters are function arguments not present in the path. Optional ones use `= None` as default.
- `response_model=` on a route decorator tells FastAPI to validate and serialize the return value against a Pydantic model — extra fields are stripped, missing required fields raise an error.
- `RedirectResponse(url=..., status_code=302)` returns an HTTP redirect. FastAPI responses are just Starlette response objects.
- Request headers are read via `Header()` from `fastapi`. FastAPI auto-converts underscores to hyphens when matching header names (e.g. `user_agent` → `User-Agent`).
- `Annotated[type, Header()]` is the modern (0.100+) way to declare header dependencies — cleaner than positional `= Header()`.

### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `@app.get(path)` | Registers a GET route handler |
| `response_model=ModelClass` | Validates and shapes the response via Pydantic |
| `RedirectResponse(url, status_code)` | Returns an HTTP redirect response |
| `Header()` | Reads a request header; auto-maps underscores to hyphens |
| `Annotated[T, Header()]` | Modern style for declaring header params |
| `str \| None = None` | Python 3.10+ union syntax for optional params |

---

## Q&A

_Add questions and answers as they come up during learning._

---

## 2. Pydantic Models & Validation

### Key Concepts

- Separate request and response models — request models validate incoming data, response models shape outgoing data. Don't mix concerns.
- `AnyHttpUrl` is a Pydantic type that validates URL format automatically. Returns a URL object, not a plain `str` — wrap in `str()` if you need string operations.
- `Field()` adds constraints to a field: `min_length`, `max_length`, `pattern` (regex), `gt`, `lt`, etc.
- Optional fields with constraints: `field: str | None = Field(default=None, min_length=3)` — constraints only run when value is not `None`.
- Regex patterns in `Field(pattern=...)` must be anchored (`^...$`) to match the full value, not just a substring.
- `@model_validator(mode="after")` runs after all fields are validated. `self` gives access to all field values. Must return `self`.
- Nested models: declare a `BaseModel` as the type of another model's field. FastAPI handles nested JSON automatically.
- `EmailStr` from Pydantic validates email format. Requires `pip install pydantic[email]`.
- Response models don't need validation constraints — those belong on request models only.
- `return payload` in a route handler works when the return type matches `response_model` — FastAPI serializes the Pydantic object directly.

### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `AnyHttpUrl` | Pydantic type that validates HTTP/HTTPS URLs |
| `EmailStr` | Pydantic type that validates email format |
| `Field(min_length, max_length, pattern)` | Adds constraints to a single field |
| `@model_validator(mode="after")` | Cross-field validation after all fields are validated |
| `raise ValueError(...)` inside validator | Pydantic converts this to a 422 response automatically |
| Nested `BaseModel` as field type | Enables nested JSON body parsing |

---

## 3. Dependency Injection

### Key Concepts

- `Depends(fn)` tells FastAPI to call `fn` before the route handler and inject the result. The route function declares *what it needs*, not how to get it.
- Dependencies are plain functions — no special class or decorator needed.
- `yield` dependencies split into setup (before yield) and teardown (after yield). Teardown runs after the response is sent. Used for DB sessions, file handles, etc.
- `Annotated[Type, Depends(fn)]` is the modern style — define a type alias once, reuse across multiple routes. Cleaner than repeating `= Depends(fn)` in every signature.
- Dependencies can depend on other dependencies — FastAPI builds the full graph and resolves it automatically.
- Use `HTTPException(status_code)` inside dependencies to return HTTP errors. `raise ValueError` produces a 500, not a 4xx.
- Return typed Pydantic model instances from dependencies instead of plain dicts — consumers get typed objects with known fields, not opaque dicts.
- `Header(...)` with ellipsis makes a header required — FastAPI returns 422 before your code runs if it's missing. `Header()` without ellipsis makes it optional (defaults to `None`).

### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `Depends(fn)` | Declares a dependency — FastAPI calls `fn` and injects the result |
| `yield` in a dependency | Splits dependency into setup + teardown around the request lifecycle |
| `Annotated[T, Depends(fn)]` | Modern type alias pattern for reusable dependencies |
| `HTTPException(status_code)` | Raises an HTTP error from a dependency or route |
| `Header(...)` | Reads a required request header; `...` makes it required |

---

## 4. Async Database (SQLAlchemy + Alembic)

### Key Concepts

- `create_async_engine` creates the connection pool once at module level — never inside a request handler or dependency.
- `async_sessionmaker` is a session factory. Call it to get an `AsyncSession` per request.
- `expire_on_commit=False` — prevents SQLAlchemy from expiring ORM object attributes after commit, which would trigger extra DB queries in an async context.
- `get_db()` yield dependency opens a session, yields it to the route, session closes automatically via `async with`.
- ORM models use SQLAlchemy 2.0 style: `Mapped[type]` for column type annotations, `mapped_column()` for column config. `Mapped[str]` = NOT NULL, `Mapped[str | None]` = nullable.
- `__tablename__` is required on every ORM model — tells SQLAlchemy which table it maps to.
- `server_default=func.now()` — delegates timestamp default to the DB's `NOW()`. Don't use `default=datetime.utcnow` for server-side defaults.
- SQLAlchemy 2.0 query style: `select(Model).where(...)`, then `await session.execute(query)`.
- `.scalars().all()` — returns a list of ORM objects. `.scalar_one_or_none()` — returns a single object or `None`.
- After `session.add()` and `await session.commit()`, call `await session.refresh(obj)` to reload DB-generated fields (`id`, `created_at`) back into the object.
- `ConfigDict(from_attributes=True)` on a Pydantic model allows it to read from ORM object attributes instead of dicts. Required when returning ORM objects from routes with `response_model=`.
- Alembic manages schema migrations. `alembic revision --autogenerate` detects model changes. `alembic upgrade head` applies them.
- Alembic's `env.py` needs to be configured for async: use `async_engine_from_config` + `run_sync()` pattern. Import all ORM models before `target_metadata` so autogenerate can detect them.
- `asyncpg` requires `greenlet` as a dependency — install it explicitly.

### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `create_async_engine(url, echo=True)` | Creates async connection pool; `echo=True` logs SQL |
| `async_sessionmaker(bind, class_, expire_on_commit)` | Session factory for creating `AsyncSession` instances |
| `AsyncSession` | Async unit of work — run queries, commit, rollback |
| `DeclarativeBase` | Base class for ORM models |
| `AsyncAttrs` | Mixin that makes ORM relationship loading async-compatible |
| `Mapped[T]` + `mapped_column()` | SQLAlchemy 2.0 column declaration style |
| `server_default=func.now()` | DB-side default for timestamp columns |
| `select(Model).where(...)` | SQLAlchemy 2.0 query style |
| `.scalar_one_or_none()` | Returns single result or None — use for ID lookups |
| `await session.refresh(obj)` | Reloads DB-generated fields after commit |
| `ConfigDict(from_attributes=True)` | Lets Pydantic read from ORM object attributes |
| `alembic init migrations` | Initialises Alembic in a project |
| `alembic revision --autogenerate -m "..."` | Generates migration from ORM model changes |
| `alembic upgrade head` | Applies all pending migrations |

---

## 5. Authentication (JWT)

### Key Concepts

- `passlib` with `CryptContext(schemes=["bcrypt"])` handles password hashing. `pwd_context.hash()` hashes, `pwd_context.verify()` checks. Use `bcrypt==4.0.1` — bcrypt 5.x is incompatible with passlib 1.7.4.
- Never store raw passwords. Never return hashed passwords in responses — keep `password` out of response models entirely.
- `python-jose` handles JWT. `jwt.encode(payload, key, algorithm)` creates a token. `jwt.decode(token, key, algorithms)` verifies and decodes it.
- The `exp` claim must be a `datetime` object or Unix timestamp integer — not a string. `python-jose` automatically rejects expired tokens during decode.
- `sub` (subject) is the standard claim for storing the user identifier. Always store it as a string.
- `jwt.decode` raises `JWTError` for invalid signature, expired token, or malformed token. Always catch it and raise a 401 — never let it bubble as a 500.
- Define a Pydantic `Token` model and do `Token(**payload)` after decode — gives you a typed object instead of a raw dict for accessing claims.
- `OAuth2PasswordBearer` is the FastAPI-native way to declare token auth in OpenAPI docs, but reading the `Authorization` header manually with `Header(...)` and `str.removeprefix("Bearer ")` works equally well for learning.
- Return the same error message for "user not found" and "wrong password" — different messages allow email enumeration attacks.
- `Annotated[str, Depends(authenticate_jwt)]` as a type alias (`CurrentUser`) keeps route signatures clean and the dependency reusable across multiple routes.

### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `CryptContext(schemes=["bcrypt"])` | Configures passlib to use bcrypt for hashing |
| `pwd_context.hash(password)` | Hashes a plain password |
| `pwd_context.verify(plain, hashed)` | Verifies plain password against hash |
| `jwt.encode(payload, key, algorithm)` | Creates a signed JWT string |
| `jwt.decode(token, key, algorithms)` | Verifies and decodes a JWT; raises `JWTError` on failure |
| `JWTError` | Exception raised by `python-jose` for invalid/expired tokens |
| `Token(**payload)` | Constructs a typed Pydantic model from the decoded JWT dict |
| `Header(...)` | Reads a required request header (`...` makes it mandatory) |
| `str.removeprefix("Bearer ")` | Strips the Bearer prefix from the Authorization header value |

---

## 4.5 SQLAlchemy Deep-Dive (Sync → Async)

### Part A — Engine and Connections

#### Key Concepts

- `Engine` is the central source of connections to a single database and a **connection pool manager**. It maintains a pool of reusable connections. Create it once at startup — never inside a request handler or loop.
- `echo=True` logs all SQL emitted to stdout — useful during learning and debugging.
- Engine uses **lazy initialization** — it doesn't actually connect to the DB when created. The first connection happens when you first execute something.
- When SQLAlchemy connects to PostgreSQL for the first time, it runs 3 introspection queries (`pg_catalog.version()`, `current_schema()`, `standard_conforming_strings`) to configure the dialect. Not visible with SQLite.
- `engine.connect()` returns a `Connection` object. A transaction is always in progress by default (DBAPI behavior). If the `with` block exits without a commit, SQLAlchemy automatically issues a `ROLLBACK`.
- `engine.begin()` is the "begin once" style — commits automatically on clean exit, rolls back automatically if an exception is raised. All-or-nothing. Prefer this when the entire block is one logical transaction.
- `engine.connect()` is "commit as you go" — you call `conn.commit()` manually. Multiple commits mid-block are possible, so a partial commit + exception = partial data persisted. Use when you need fine-grained control.
- Bound parameters use `:param` syntax in `text()`. SQLAlchemy translates to the backend's native style — `?` for SQLite, `%(param)s` for PostgreSQL. Never string-format user input into SQL.
- In-memory SQLite (`:memory:`) is per-connection — each new `engine.connect()` gets a fresh empty DB. Use a file-based DB (`sqlite:///file.db`) if you need data to persist across connections.
- `psycopg2-binary` is the sync PostgreSQL driver. `psycopg2` (without binary) requires PostgreSQL dev headers to compile from source — use the binary variant for development.

#### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `create_engine(url, echo=True)` | Creates sync connection pool; `echo=True` logs all SQL |
| `engine.connect()` | Returns a `Connection`; "commit as you go" style |
| `engine.begin()` | Returns a `Connection`; auto-commits on success, auto-rolls back on exception |
| `conn.execute(text(...))` | Executes a raw SQL statement |
| `conn.commit()` | Commits the current transaction |
| `text("SQL :param")` | Wraps a raw SQL string; supports bound parameters via `:param` syntax |
| `result.all()` | Returns all rows as a list of named tuples |
| `psycopg2-binary` | Sync PostgreSQL DBAPI driver (pre-compiled, no system deps required) |

### Part B — Database Metadata

#### Key Concepts

- `MetaData` is a registry for all table definitions — one per app. Holds `Table` objects keyed by name.
- Core style: define tables explicitly using `Table`, `Column`, and type objects (`Integer`, `String`, etc.). Gives you full control but is more verbose.
- ORM style: subclass `DeclarativeBase`, declare mapped classes with `Mapped[T]` annotations. Cleaner, Python-typed, integrates with IDE tooling. Still creates a `Table` object under the hood — accessible via `MyClass.__table__`.
- Both styles produce the same underlying `Table` object. ORM is a layer on top of Core, not a replacement.
- `Mapped[str]` = NOT NULL column. `Mapped[str | None]` = nullable column. The Python type annotation directly controls nullability.
- `mapped_column()` is the ORM equivalent of `Column()` — use it when you need extra config (e.g. `primary_key=True`, `ForeignKey`, `String(30)`). For simple columns, `Mapped[str]` alone is enough.
- `ForeignKey("tablename.column")` declares a FK constraint. Uses the string `__tablename__` value, not the class name.
- `Base.metadata.create_all(engine)` emits `CREATE TABLE` for all mapped classes. `metadata_obj.create_all(engine)` does the same for Core tables.
- Two separate `MetaData` objects = two separate registries. Alembic's `target_metadata` can only point to one — mixing Core and ORM tables with separate metadata makes autogenerate miss half the tables. Solution: share one `MetaData` by passing it to `DeclarativeBase(metadata=shared_metadata_obj)`.
- `table.c.keys()` returns a list of column names. `table.primary_key` returns the `PrimaryKeyConstraint` object.

#### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `MetaData()` | Registry that holds all `Table` objects |
| `Table(name, metadata, *columns)` | Core-style table definition |
| `Column(name, type, ...)` | Core-style column definition |
| `DeclarativeBase` | Base class for ORM mapped classes; creates its own `MetaData` |
| `Mapped[T]` | ORM column type annotation; `T` controls nullability |
| `mapped_column(...)` | ORM column config (PK, FK, type length, etc.) |
| `ForeignKey("table.col")` | Declares a foreign key constraint |
| `metadata_obj.create_all(engine)` | Emits `CREATE TABLE` for all registered Core tables |
| `Base.metadata.create_all(engine)` | Emits `CREATE TABLE` for all ORM mapped classes |
| `table.c.keys()` | Returns list of column names |
| `table.primary_key` | Returns the `PrimaryKeyConstraint` for the table |

### Part C — Core CRUD (INSERT, SELECT, JOIN, UPDATE, DELETE)

#### Key Concepts

- `insert()`, `select()`, `update()`, `delete()` are composable Python objects — not strings. Chain methods like `.where()`, `.values()`, `.returning()` to build the statement before executing.
- `.returning(*cols)` on INSERT, UPDATE, or DELETE returns the specified columns from affected rows. Result must be consumed before the cursor is closed — call `result.all()` once and store it if you need the data later.
- When inserting rows with FK dependencies (e.g. address requires a user_id), capture the parent row's id from RETURNING before committing, then use it in the child insert. Calling `result.all()` a second time returns an empty list — the cursor is exhausted.
- Multi-row insert: pass a list of dicts to `.values([...])`. SQLAlchemy batches these into a single `INSERT ... VALUES (...), (...)` statement.
- `.where()` builds the WHERE clause. Chain multiple `.where()` calls for AND conditions. Pass multiple expressions to a single `.where()` for the same effect.
- SELECT specific columns: `select(table.c.col1, table.c.col2)` — FROM is inferred from the columns.
- JOIN: use `.join(right_table, on_clause)` on the `select()` — left side is inferred from the columns in the SELECT list. Use `.join_from(left, right, on_clause)` for explicit left side. ON clause is auto-inferred from FK constraints when unambiguous — explicit is safer and clearer.
- `result.all()` — list of named tuples. Rows support attribute access (`row.name`), index access (`row[0]`), and tuple unpacking.
- `[cached since ...]` in SQLAlchemy echo output means the query *compilation* was cached — it still hits the DB. Not a result cache.

#### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `insert(table).values(...)` | Builds an INSERT statement |
| `insert(table).values([...])` | Multi-row INSERT with a list of dicts |
| `select(table)` | Builds a SELECT for all columns |
| `select(table.c.col1, ...)` | SELECT specific columns; FROM inferred |
| `.where(condition)` | Adds a WHERE clause; chain for AND |
| `.join(right, on_clause)` | INNER JOIN; left side inferred from SELECT columns |
| `.join_from(left, right, on_clause)` | INNER JOIN with explicit left side |
| `.join(..., isouter=True)` | LEFT OUTER JOIN |
| `update(table).where(...).values(...)` | Builds an UPDATE statement |
| `delete(table).where(...)` | Builds a DELETE statement |
| `.returning(*cols)` | Returns specified columns from affected rows |
| `result.all()` | Consumes and returns all rows as named tuples; call once only |
| `result.rowcount` | Number of rows matched by WHERE (UPDATE/DELETE) |

### Part D — ORM Session and Unit of Work

#### Key Concepts

- ORM objects go through states: **transient** (created, not added) → **pending** (added to session, not flushed) → **persistent** (flushed/committed, has a DB row) → **expired** (committed, attributes cleared) → **detached** (session closed).
- `session.add(obj)` marks an object as pending. No SQL is sent yet.
- `session.flush()` sends SQL to the DB but keeps the transaction open. After flush, `obj.id` is populated via `RETURNING`. Rarely called manually — Session autoflushes before any SELECT.
- `session.commit()` commits the transaction. By default (`expire_on_commit=True`) all objects are expired — next attribute access triggers a SELECT to reload.
- `session.get(Model, pk)` checks the **identity map** first. If the object is already in memory, it returns the same Python object with no extra query. Only hits the DB if not loaded.
- To UPDATE: just mutate the attribute (`obj.name = "new"`). Session tracks it via `session.dirty`. UPDATE is emitted automatically on next flush/commit.
- To DELETE: `session.delete(obj)`. No SQL until flush. After commit, object is removed from session.
- `session.rollback()` rolls back the transaction AND expires all objects. Next attribute access re-fetches from DB.
- After rollback, `obj.__dict__` is wiped to just `_sa_instance_state`. Accessing any attribute triggers a new SELECT.
- `sessionmaker(bind=engine, expire_on_commit=False)` creates a session factory. Call it to get a new session per request. `expire_on_commit=False` prevents expiry after commit — required in async context since expired attributes can't trigger lazy SELECTs mid-await.
- Python `with` blocks do NOT create a new variable scope — variables defined inside are accessible outside. So `latest_user_id` set inside a `with Session()` block is accessible in the next `with` block.
- After session closes, objects become **detached**. Accessing attributes raises `DetachedInstanceError` unless `expire_on_commit=False` was set (attributes stay populated).

#### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `Session(engine)` | Creates a session directly; use as context manager |
| `sessionmaker(bind=engine, expire_on_commit=False)` | Session factory — call it to get a new `Session` |
| `session.add(obj)` | Marks object as pending; queued for INSERT on flush |
| `session.flush()` | Sends pending SQL to DB; transaction stays open |
| `session.commit()` | Commits transaction; expires objects by default |
| `session.rollback()` | Rolls back transaction; expires all objects |
| `session.get(Model, pk)` | Returns object from identity map or DB by primary key |
| `session.delete(obj)` | Marks object for DELETE on next flush |
| `session.new` | Set of pending (not yet flushed) objects |
| `session.dirty` | Set of persistent objects with uncommitted changes |
| `expire_on_commit=False` | Keep attributes populated after commit; required for async |


### Part E — Async SQLAlchemy

#### Key Concepts

- `create_async_engine` with `postgresql+asyncpg://` URL is the async equivalent of `create_engine`. Same "create once at startup" rule applies.
- `async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)` is the async session factory. `expire_on_commit=False` is mandatory in async — expired attributes can't trigger a lazy SELECT mid-await.
- All session operations must be awaited: `await session.flush()`, `await session.commit()`, `await session.rollback()`, `await session.get()`, `await session.delete()`.
- `AsyncAttrs` mixin must be added to `DeclarativeBase` for async-safe attribute access. Without it, any attribute access that triggers a lazy load hits a `MissingGreenlet` error.
- Rollback expires all objects regardless of `expire_on_commit`. After rollback, accessing an attribute directly will trigger a lazy load — which fails synchronously in async context. Always re-fetch with `await session.get()` after rollback instead of relying on the expired object.
- `AsyncAttrs` provides `await obj.awaitable_attrs.field` as an escape hatch for one-off async attribute access — but explicit re-fetch is the cleaner pattern in practice.
- Identity map works the same as sync: `session.get(Model, pk)` returns the cached Python object if already loaded in the current session — no extra SELECT.
- The engine → pool → connection → session chain is identical to sync. `AsyncSession` borrows a connection from the async pool only when it needs to execute SQL.

#### APIs / Tools Learned

| API / Tool | What it does |
|---|---|
| `create_async_engine(url, echo=True)` | Creates async connection pool for PostgreSQL via asyncpg |
| `async_sessionmaker(bind, class_, expire_on_commit)` | Async session factory |
| `AsyncSession` | Async unit of work — all operations must be awaited |
| `AsyncAttrs` | Mixin for `DeclarativeBase` — enables async-safe attribute access |
| `await session.flush()` | Sends pending SQL to DB; transaction stays open |
| `await session.commit()` | Commits transaction |
| `await session.rollback()` | Rolls back transaction; expires all objects |
| `await session.get(Model, pk)` | Fetches by PK from identity map or DB |
| `await session.delete(obj)` | Marks object for DELETE on next flush |
| `obj.awaitable_attrs.field` | Async attribute access escape hatch (prefer re-fetch instead) |
| `asyncio.run(main())` | Entry point for running an async function from a sync script |

---

## 5.5 Alembic Deep-Dive

### Part A — Structure & Version Chain

#### Key Concepts

- `alembic.ini` — config file. Holds `sqlalchemy.url` and points to the migrations directory.
- `migrations/env.py` — the script Alembic runs on every command. Configures the engine, sets `target_metadata`, and calls `run_migrations_online()` or `run_migrations_offline()`.
- `migrations/script.py.mako` — Jinja template used to generate new revision files. Modifying this changes what boilerplate new revisions get.
- `migrations/versions/` — one `.py` file per revision. Each file has `revision`, `down_revision`, `upgrade()`, and `downgrade()`.
- The version chain is a linked list: each revision's `down_revision` points to its parent. `head` is the latest. `base` is the start (no parent).
- `alembic_version` table — Alembic creates this in your DB. Stores one row: the currently applied revision ID. Alembic reads it to know where you are.
- `alembic history` — prints the full chain oldest to newest.
- `alembic current` — queries `alembic_version` to show where the live DB is right now.
- `alembic heads` — shows the latest revision(s) in the chain. Matches `current` when fully up to date; diverges after a downgrade.

#### APIs / Tools Learned

| Command | What it does |
|---|---|
| `alembic history` | Lists all revisions in the chain |
| `alembic current` | Shows the revision the live DB is currently at |
| `alembic heads` | Shows the latest revision(s) in the chain |

---

### Part B — env.py Internals

#### Key Concepts

- `env.py` runs on every Alembic command — it's the bridge between your models and the DB.
- `target_metadata = Base.metadata` — points Alembic at your ORM model registry. Autogenerate diffs this against the live DB schema.
- All models must be imported before `target_metadata` is set. If a model isn't imported, autogenerate can't see it and will generate a `drop_table` for it.
- Async `env.py` pattern: define `run_async_migrations()` as an async function, then use `asyncio.run()` + `connectable.run_sync(do_run_migrations)` to run migrations synchronously inside the async engine. Alembic's migration operations are sync-only — they can't be awaited directly.
- `run_migrations_online()` — connects to a live DB and applies migrations. Used in normal operation.
- `run_migrations_offline()` — generates SQL scripts without connecting. Used for reviewing migrations before applying.

---

### Part C — Migration Operations

#### Key Concepts

- `alembic upgrade head` — applies all pending migrations from current to head.
- `alembic downgrade -1` — rolls back one step. Alembic runs `downgrade()` of the current revision.
- `alembic downgrade base` — rolls back all migrations to the initial state. Alembic walks the chain one step at a time — you'll see one log line per migration.
- `alembic revision -m "message"` — creates an empty revision file with no `upgrade()`/`downgrade()` body. Use this for manual migrations.
- `alembic revision --autogenerate -m "message"` — detects model changes and generates the body automatically. Misses: renames (sees drop + add instead), some constraints, data migrations.
- Column rename limitation: autogenerate sees a rename as `drop_column` + `add_column` — existing data is lost. Must write a manual `op.alter_column(..., new_column_name=...)`.
- `op.add_column(table, Column(...))` — adds a column in upgrade.
- `op.drop_column(table, column_name)` — removes a column in downgrade.
- `op.alter_column(table, col, ...)` — modifies a column (rename, type change, nullability).
- `server_default` vs `default`:
  - `server_default="value"` — the DB fills in the value. Works during `ALTER TABLE` for existing rows.
  - `default=value` — Python/SQLAlchemy fills in the value when you do `session.add(obj)`. The DB knows nothing about it.
  - Adding a `NOT NULL` column to a table with existing rows requires `server_default` — `default` alone causes a "column contains null values" error because the DB can't backfill.

#### APIs / Tools Learned

| Command / API | What it does |
|---|---|
| `alembic upgrade head` | Applies all pending migrations |
| `alembic downgrade -1` | Rolls back one migration |
| `alembic downgrade base` | Rolls back all migrations |
| `alembic revision -m "..."` | Creates an empty manual revision |
| `op.add_column(table, Column(...))` | Adds a column |
| `op.drop_column(table, col_name)` | Drops a column |
| `op.alter_column(table, col, ...)` | Alters a column (rename, type, nullability) |
| `server_default="value"` | DB-level default — used for backfilling existing rows |
| `default=value` | Python-level default — SQLAlchemy only, DB unaware |

## Q&A

### Why does `alembic downgrade base` show one log line per migration?
Alembic always walks the version chain one step at a time — it can't skip revisions. Each migration's `downgrade()` runs in reverse order. `base` just means "keep going until there's no more `down_revision`".

### Why can't autogenerate detect column renames?
It has no concept of intent. It sees that a column with the old name is gone and a new column appeared. From its perspective, that's a delete + add. To rename, you must write a manual `op.alter_column(..., new_column_name=...)` migration.

### When do you use `server_default` vs `default`?
Use `server_default` when the column is `NOT NULL` and the table already has rows — the DB needs a value to backfill immediately during `ALTER TABLE`. Use `default` in Python for application-level defaults when inserting new rows via SQLAlchemy (e.g. generating UUIDs, timestamps in Python). In practice, use `server_default` for timestamps and booleans in migrations, and `default` for Python-generated values like UUIDs.
