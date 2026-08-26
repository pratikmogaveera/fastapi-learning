# FastAPI Learning Path

Structured exercises to learn FastAPI 0.141 from scratch — building toward the URL shortener project.

## Purpose

Learn FastAPI concepts hands-on through small, focused exercises. Each phase maps directly to a feature used in the URL shortener. Not a tutorial copy-paste — exercises are written from scratch after understanding the concept.

## Tech Stack

- **Framework:** FastAPI 0.141+
- **Runtime:** Python 3.12+
- **Package manager:** uv
- **DB:** PostgreSQL (via SQLAlchemy async)
- **Cache:** Redis
- **Testing:** pytest + httpx (TestClient)
- **Server:** Uvicorn

## How to Run

> **Want a clean start?** Switch to the [  `clean/starter`  ](https://github.com/pratikmogaveera/fastapi-learning/tree/clean/starter) branch — it has all phases set up with TODOs and no solutions.

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtualenv and install deps
uv venv
source .venv/bin/activate
uv pip install "fastapi[standard]" uvicorn sqlalchemy asyncpg alembic redis pytest httpx

# Run any phase
cd phase-01-routing
uvicorn main:app --reload
```

## File Structure

```
fastapi-learning/
├── README.md               — this file
├── PLAN.md                 — phase-by-phase learning roadmap
├── NOTES.md                — concepts, Q&A, key takeaways
├── phase-00-python-basics/ — type hints, classes, decorators, async/await
├── phase-01-routing/       — path params, query params, response models
├── phase-02-pydantic/      — request validation, custom validators, nested models
├── phase-03-dependency-injection/ — deps, shared deps, db session injection
├── phase-04-async-db/      — SQLAlchemy async, Alembic migrations
├── phase-05-auth/          — JWT auth, password hashing, protected routes
├── phase-06-background-tasks/ — FastAPI BackgroundTasks, ARQ worker
├── phase-07-middleware/    — custom middleware, CORS, request logging
├── phase-08-testing/       — pytest, TestClient, async test setup
└── phase-09-redis/         — Redis caching, rate limiting
```

## Progress

- [x] Phase 0 — Python Basics for FastAPI
- [x] Phase 1 — Routing & Request Handling
- [x] Phase 2 — Pydantic Models & Validation
- [x] Phase 3 — Dependency Injection
- [x] Phase 4 — Async Database (SQLAlchemy + Alembic)
- [ ] Phase 5 — Authentication (JWT)
- [ ] Phase 6 — Background Tasks & Workers
- [ ] Phase 7 — Middleware
- [ ] Phase 8 — Testing
- [ ] Phase 9 — Redis Caching & Rate Limiting

## Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com)
- [Pydantic v2 Docs](https://docs.pydantic.dev/latest/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/)
- [ARQ Docs](https://arq-docs.helpmanual.io/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
