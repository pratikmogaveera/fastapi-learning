from fastapi import FastAPI

app = FastAPI()

# EXERCISE 1 — Basic route
# Create a GET /items/{item_id} endpoint that:
# - Accepts item_id as an integer path parameter
# - Accepts an optional query param `q` (string, default None)
# - Returns {"item_id": item_id, "q": q}
# Test: GET /items/42?q=hello → {"item_id": 42, "q": "hello"}
# Test: GET /items/abc → 422 Unprocessable Entity (FastAPI validates the type)

# TODO: implement here


# EXERCISE 2 — Response model
# Define a Pydantic model `ItemResponse` with fields: id (int), name (str), price (float)
# Create a GET /items/{item_id}/detail endpoint that returns a hardcoded ItemResponse
# Use response_model= to enforce the shape
# Verify: /docs shows the response schema

# TODO: implement here


# EXERCISE 3 — Redirect response
# Create a GET /go endpoint that accepts a `url` query param
# Return a 302 redirect to that URL
# Hint: from fastapi.responses import RedirectResponse

# TODO: implement here


# EXERCISE 4 — Read a request header
# Create a GET /whoami endpoint
# Read the User-Agent header from the request
# Return {"user_agent": "...value..."}
# Hint: use Header() from fastapi

# TODO: implement here
