from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


@app.get("/health", summary="A test endpoint to check if the app is running.")
async def root():
    return {"message": "Everything working as expected."}


# EXERCISE 1 — Basic route
# Create a GET /items/{item_id} endpoint that:
# - Accepts item_id as an integer path parameter
# - Accepts an optional query param `q` (string, default None)
# - Returns {"item_id": item_id, "q": q}
# Test: GET /items/42?q=hello → {"item_id": 42, "q": "hello"}
# Test: GET /items/abc → 422 Unprocessable Entity (FastAPI validates the type)


@app.get("/items/{item_id}", summary="Get endpoint that captures path and query parameters.")
async def get_item_by_id(item_id: int, q: str | None = None):
    response: dict[str, int | str | None] = {"item_id": item_id, "q": q}

    return response


# EXERCISE 2 — Response model
# Define a Pydantic model `ItemResponse` with fields: id (int), name (str), price (float)
# Create a GET /items/{item_id}/detail endpoint that returns a hardcoded ItemResponse
# Use response_model= to enforce the shape
# Verify: /docs shows the response schema


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float


@app.get("/items/{item_id}/detail", response_model=ItemResponse)
async def get_items_details(item_id: int):
    return {"id": item_id, "name": "Item Name", "price": 1.2}


# EXERCISE 3 — Redirect response
# Create a GET /go endpoint that accepts a `url` query param
# Return a 302 redirect to that URL
# Hint: from fastapi.responses import RedirectResponse


@app.get("/go")
async def go_to_url(url: str):
    return RedirectResponse(url=url, status_code=302)


# EXERCISE 4 — Read a request header
# Create a GET /whoami endpoint
# Read the User-Agent header from the request
# Return {"user_agent": "...value..."}
# Hint: use Header() from fastapi


@app.get("/whoami")
async def who_am_i(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}
