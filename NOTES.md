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
