import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

# EXERCISE 1 — Basic dependency
# Create a dependency function `get_request_id()` that returns a random UUID string
# Inject it into a GET /ping endpoint
# Return {"request_id": "...", "status": "ok"}
# Hint: use Depends() from fastapi


def get_request_id() -> uuid.UUID:
    return uuid.uuid4()


@app.get("/ping")
async def ping(id=Depends(get_request_id)):
    return {"request_id": id, "status": "ok"}


# EXERCISE 2 — Auth dependency
# Create a dependency `get_current_user(authorization: str = Header(...))` that:
#   - Reads the Authorization header
#   - Expects the value to be "Bearer secret-token"
#   - Returns {"user_id": 1, "email": "test@example.com"} if valid
#   - Raises HTTPException(401) if missing or wrong
#
# Inject it into GET /me and return the user
# Test: curl with and without the header


class User(BaseModel):
    id: int
    name: str


def get_current_user(authorization: str = Header(...)) -> User:
    if authorization == "Bearer secret-token":
        return User(id=1, name="Pratik")
    else:
        raise HTTPException(401)


@app.get("/me", response_model=User)
async def whoami(user=Depends(get_current_user)):
    return user


# EXERCISE 3 — Shared dependency with Annotated
# Rewrite the auth dependency using the Annotated pattern:
#   CurrentUser = Annotated[dict, Depends(get_current_user)]
# Use CurrentUser as a type hint in /dashboard
# This is the modern FastAPI style (0.95+)


class DashboardResponse(BaseModel):
    id: int
    total_amount: int


CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/dashboard", response_model=DashboardResponse)
async def dashboard(user: CurrentUser):
    return {"id": user.id, "total_amount": 100}


# EXERCISE 4 — Yield dependency (simulating DB session)
# Create a `get_db()` dependency that:
#   - "Opens" a fake session (just print "DB session opened")
#   - Yields a mock dict {"session": "active"}
#   - "Closes" it after the request (print "DB session closed")
#
# Use it in a GET /data endpoint
# Observe the open/close prints in the terminal


def get_db():
    print("DB: Connection opened.")
    yield {"session": "active"}
    print("DB: Connection closed.")


DBConn = Annotated[dict, Depends(get_db)]


@app.get("/data")
async def get_data(connection: DBConn):
    return {"total_amount": 100, "total_users": 5}
