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
