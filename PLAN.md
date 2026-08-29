# FastAPI Learning Path — Plan

Learn FastAPI 0.141 through exercises that directly map to what you'll need for the URL shortener project. Each phase is self-contained and builds on the previous.

---

## 1. Routing & Request Handling

**Goal:** Understand how FastAPI handles incoming HTTP requests — path params, query params, headers, and response models.

**Tasks:**
- Create a `GET /items/{item_id}` endpoint with path param validation
- Add optional query params with defaults
- Return a typed response model using `response_model=`
- Read a custom request header
- Return different HTTP status codes

**Key Concepts:**
- `@app.get`, `@app.post`, etc. decorators
- Path parameters vs query parameters
- `Response`, `JSONResponse`, `RedirectResponse`
- `status_code` parameter
- Auto-generated docs at `/docs` (Swagger) and `/redoc`

**Done when:** A `/items/{id}` endpoint validates types, rejects bad input with a 422, and returns a typed response. A `/redirect` endpoint returns a 302.

---

## 2. Pydantic Models & Validation

**Goal:** Master Pydantic v2 for request body validation, response shaping, and custom validators.

**Tasks:**
- Define a `CreateItem` request model and a `ItemResponse` response model
- Add field validators (min length, regex, custom)
- Use `model_validator` for cross-field validation
- Use `Field(alias=...)` and `model_config` for serialization control
- Nest models (e.g. `Address` inside `User`)

**Key Concepts:**
- `BaseModel`, `Field`, `model_validator`, `field_validator`
- `model_config` (Pydantic v2 replaces `class Config`)
- Request body vs response model separation
- `exclude_unset`, `model_dump()`

**Done when:** A `POST /users` endpoint accepts a nested body, validates it, and returns a shaped response — rejecting invalid input with clear error messages.

---

## 3. Dependency Injection

**Goal:** Understand FastAPI's DI system — the equivalent of NestJS providers but function-based.

**Tasks:**
- Create a simple `get_db()` dependency that yields a mock DB session
- Create a `get_current_user()` dependency that reads an `Authorization` header
- Use `Depends()` in a route
- Create a shared dependency used by multiple routes
- Use `Annotated` type hints for cleaner dep declarations (FastAPI 0.100+ style)

**Key Concepts:**
- `Depends()` and `yield` dependencies
- Dependency lifecycle (per-request)
- `Annotated[type, Depends(fn)]` pattern
- Nested dependencies
- Why DI > global state

**Done when:** A protected route uses `Depends(get_current_user)` and a DB route uses `Depends(get_db)` — both injected cleanly without touching global state.

---

## 4. Async Database (SQLAlchemy + Alembic)

**Goal:** Connect to PostgreSQL using async SQLAlchemy and manage schema with Alembic migrations.

**Tasks:**
- Set up `AsyncEngine` and `AsyncSession` with SQLAlchemy 2.0
- Define a `Link` model (ORM)
- Wire `get_db()` dependency to yield an `AsyncSession`
- Write async CRUD functions (create, get by id, list)
- Set up Alembic, write and run a migration

**Key Concepts:**
- `create_async_engine`, `AsyncSession`, `async_sessionmaker`
- ORM `select()` queries (SQLAlchemy 2.0 style)
- `await session.commit()`, `await session.refresh()`
- Alembic `env.py` with async setup
- Connection pooling (`pool_size`, `max_overflow`)

**Done when:** A `POST /links` and `GET /links/{id}` endpoint reads/writes to a real PostgreSQL DB using async SQLAlchemy. Schema managed via Alembic migration.

---

## 4.5 SQLAlchemy Deep-Dive (Sync → Async)

**Goal:** Understand SQLAlchemy from the ground up by reading the official tutorial and implementing each concept side by side. No FastAPI. Standalone Python scripts only.

**Reference:** https://docs.sqlalchemy.org/en/20/tutorial/index.html

---

**Part A — Engine and Connections**
_Doc section: "Establishing Connectivity" + "Working with Transactions and the DBAPI"_

Read both sections, then write `part_a.py`:
- Create a sync engine using `create_engine` with `echo=True` (use SQLite `:memory:` for now)
- Open a `Connection` using `engine.connect()` as a context manager
- Run a raw SQL query using `text()` and print the result
- Insert a row using `text()` with bound parameters and commit ("commit as you go" style)
- Repeat the insert using `engine.begin()` ("begin once" style)
- Select rows back and iterate over the `Result` object — try tuple unpacking, index access, and attribute access
- Switch to PostgreSQL URL and confirm it still works

**Key concepts from this part:**
- Engine = connection pool, created once at startup, never inside a request
- `Connection` = one physical DB connection, short-lived, always use as context manager
- Transaction is always in progress by default — you must explicitly commit
- `Result` rows behave like named tuples — three ways to access column values
- `text()` uses `:param` style for bound parameters (never string-format user input)

---

**Part B — Database Metadata**
_Doc section: "Working with Database Metadata"_

Read the section, then write `part_b.py`:
- Define a `user_account` table using Core style: `MetaData`, `Table`, `Column`
- Add a second `address` table with a `ForeignKey` to `user_account`
- Emit DDL using `metadata_obj.create_all(engine)`
- Inspect `user_table.c.keys()` and `user_table.primary_key`
- Redefine the same two tables using ORM Declarative style: `DeclarativeBase`, `Mapped`, `mapped_column`
- Emit DDL using `Base.metadata.create_all(engine)`
- Confirm both approaches produce the same tables

**Key concepts from this part:**
- `MetaData` is the registry for all table definitions — one per app
- Core `Table` and ORM `DeclarativeBase` both produce the same underlying `Table` object
- `Mapped[str]` = NOT NULL, `Mapped[str | None]` = nullable
- `Base.metadata.create_all()` is fine for scripts/tests; use Alembic for real apps

---

**Part C — Core CRUD (INSERT, SELECT, UPDATE, DELETE)**
_Doc sections: "Using INSERT Statements", "Using SELECT Statements", "Using UPDATE and DELETE Statements"_

Read all three sections, then write `part_c.py` (using the tables from Part B):
- Insert a single row using `insert(user_table).values(...)`
- Insert multiple rows using `executemany` style (list of dicts)
- Select all rows using `select(user_table)`
- Add a `WHERE` clause using `.where()`
- Select specific columns only
- Join `user_account` and `address` tables
- Update a row using `update(user_table).where(...).values(...)`
- Delete a row using `delete(user_table).where(...)`

**Key concepts from this part:**
- Core `insert()`, `select()`, `update()`, `delete()` are composable Python objects — not strings
- `.where()` builds the WHERE clause — chain multiple for AND conditions
- `result.scalars().all()` vs `result.all()` vs `result.scalar_one_or_none()` — know when to use each

---

**Part D — ORM Session and Unit of Work**
_Doc section: "Data Manipulation with the ORM"_

Read the section, then write `part_d.py` (using ORM mapped classes from Part B):
- Create a `Session` using `Session(engine)` as context manager
- Add a `User` object using `session.add()`, observe it's in `session.new` (pending state)
- Call `session.flush()` manually — observe the INSERT happens but transaction not committed
- Call `session.commit()` — observe the object gets its `id` populated
- Fetch the same object back using `session.get(User, id)` (identity map)
- Update the object by mutating its attribute and committing
- Delete the object using `session.delete(obj)` and committing
- Try `session.rollback()` — observe the change is undone
- Replace manual `Session(engine)` with `sessionmaker` factory

**Key concepts from this part:**
- Session = unit of work. Tracks all pending changes in memory until flush/commit
- `session.add()` → pending. `flush()` → SQL sent but not committed. `commit()` → persisted
- Identity map: `session.get(User, 1)` returns the same Python object if already loaded — no extra query
- `expire_on_commit=True` (default) — after commit, accessing an attribute triggers a lazy SELECT
- `sessionmaker` is a factory — call it to get a new `Session` instance

---

**Part E — Async SQLAlchemy**

After completing Parts A–D, rewrite `part_d.py` as `part_e.py` using async:
- Replace `create_engine` → `create_async_engine` with `postgresql+asyncpg://` URL
- Replace `Session` → `AsyncSession`, `sessionmaker` → `async_sessionmaker`
- Wrap all DB calls in `async def` functions, `await` every execute/commit/refresh
- Set `expire_on_commit=False` on the session factory — understand why it's required here
- Confirm the same CRUD operations work

**Key concepts from this part:**
- `asyncpg` is the async PostgreSQL driver — SQLAlchemy calls it under the hood
- `AsyncSession` doesn't support lazy loading — expired attributes can't trigger a SELECT mid-await
- `expire_on_commit=False` prevents expiry so you can safely access attributes after commit without an extra query
- `async_sessionmaker` is the async equivalent of `sessionmaker`

---

**Key Concepts (summary)**

- Engine = connection pool manager (one per app, created once at startup)
- Connection = one physical DB connection borrowed from the pool (short-lived)
- Session = unit of work — tracks ORM object changes, not the same as a connection
- Session borrows a Connection only when it needs to execute SQL
- `sessionmaker` / `async_sessionmaker` = session factory, call it to get a new session per request
- `asyncpg` = the async PostgreSQL DBAPI driver used by SQLAlchemy's async engine

**Done when:** You can write sync and async CRUD scripts from scratch. You can explain the engine → pool → connection → session chain in your own words without referencing code.

---

## 5. Authentication (JWT)

**Goal:** Implement JWT-based auth — register, login, and protect routes.

**Tasks:**
- Hash passwords with `bcrypt` (via `passlib`)
- Issue JWT on login using `python-jose`
- Write a `get_current_user` dependency that decodes the token
- Protect a route with it
- Return 401 on invalid/expired token

**Key Concepts:**
- `passlib` for password hashing
- `python-jose` for JWT encode/decode
- `OAuth2PasswordBearer` scheme
- Token payload (sub, exp claims)
- HTTPException with proper status codes

**Done when:** `POST /auth/login` returns a JWT. A protected `GET /me` endpoint returns the current user or 401 if token is missing/invalid.

---

## 6. Background Tasks & Workers

**Goal:** Run work outside the request lifecycle — both FastAPI's built-in `BackgroundTasks` and a proper async queue with ARQ.

**Tasks:**
- Use `BackgroundTasks` to log a click after returning a redirect response
- Set up ARQ with Redis
- Define an ARQ worker function (geo lookup + mock DB write)
- Enqueue a job from a route handler
- Run the worker separately

**Key Concepts:**
- `BackgroundTasks` — when to use (simple fire-and-forget in same process)
- ARQ — when to use (separate process, retries, observability)
- `await asyncio.sleep()` to simulate async work
- Worker startup with `arq.run_worker`

**Done when:** A `GET /{short_code}` redirect endpoint returns the response immediately, then fires a background job that "processes" click data (logged to console). Worker runs in a separate terminal.

---

## 7. Middleware

**Goal:** Intercept requests and responses globally — logging, CORS, and custom headers.

**Tasks:**
- Add request logging middleware (log method, path, response time)
- Configure CORS with `CORSMiddleware`
- Add a custom `X-Request-ID` header to every response
- Write a middleware that rejects requests missing a required header

**Key Concepts:**
- `@app.middleware("http")` decorator
- `BaseHTTPMiddleware` vs pure ASGI middleware
- `request.state` for passing data across middleware → route
- Middleware execution order
- CORS preflight handling

**Done when:** Every request logs method + path + response time. CORS headers are present. Each response has an `X-Request-ID`.

---

## 8. Testing

**Goal:** Write proper unit and integration tests for FastAPI routes.

**Tasks:**
- Set up `pytest` with `httpx.AsyncClient` and `ASGITransport`
- Write tests for a CRUD endpoint (create, get, 404 case)
- Override a dependency in tests (mock DB session)
- Test an auth-protected route (valid token, missing token, expired token)
- Use `pytest` fixtures for client setup and DB teardown

**Key Concepts:**
- `AsyncClient` with `ASGITransport` (replaces deprecated `TestClient` for async)
- `app.dependency_overrides` for mocking
- `pytest.fixture` with `scope`
- Testing error cases explicitly
- Test isolation (no shared state between tests)

**Done when:** A test suite covers happy path + error cases for at least one full CRUD resource. Auth tests pass for valid and invalid token scenarios.

---

## 9. Redis Caching & Rate Limiting

**Goal:** Use Redis for caching hot data and implementing per-user rate limiting.

**Tasks:**
- Connect to Redis using `redis-py` async client
- Cache a DB lookup result in Redis with a TTL
- Invalidate cache on update
- Implement a sliding window rate limiter using Redis `INCR` + `EXPIRE`
- Apply rate limit as a dependency on a route

**Key Concepts:**
- `redis.asyncio` client
- `await redis.get()`, `await redis.set()`, `await redis.incr()`
- Cache-aside pattern
- Sliding window vs fixed window rate limiting
- Using `Depends()` for rate limit enforcement

**Done when:** A `GET /{short_code}` lookup hits Redis first and only falls back to DB on cache miss. A rate-limited endpoint returns 429 after N requests in a window.
