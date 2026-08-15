from fastapi import FastAPI

app = FastAPI()

# EXERCISE 1 — Basic dependency
# Create a dependency function `get_request_id()` that returns a random UUID string
# Inject it into a GET /ping endpoint
# Return {"request_id": "...", "status": "ok"}
# Hint: use Depends() from fastapi

# TODO: implement here


# EXERCISE 2 — Auth dependency
# Create a dependency `get_current_user(authorization: str = Header(...))` that:
#   - Reads the Authorization header
#   - Expects the value to be "Bearer secret-token"
#   - Returns {"user_id": 1, "email": "test@example.com"} if valid
#   - Raises HTTPException(401) if missing or wrong
#
# Inject it into GET /me and return the user
# Test: curl with and without the header

# TODO: implement here


# EXERCISE 3 — Shared dependency with Annotated
# Rewrite the auth dependency using the Annotated pattern:
#   CurrentUser = Annotated[dict, Depends(get_current_user)]
# Use CurrentUser as a type hint in two different routes — /me and /dashboard
# This is the modern FastAPI style (0.95+)

# TODO: implement here


# EXERCISE 4 — Yield dependency (simulating DB session)
# Create a `get_db()` dependency that:
#   - "Opens" a fake session (just print "DB session opened")
#   - Yields a mock dict {"session": "active"}
#   - "Closes" it after the request (print "DB session closed")
#
# Use it in a GET /data endpoint
# Observe the open/close prints in the terminal

# TODO: implement here
