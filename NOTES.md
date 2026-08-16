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
