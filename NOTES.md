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