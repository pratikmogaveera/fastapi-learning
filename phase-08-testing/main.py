from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserPayload(BaseModel):
  name: str


class User(BaseModel):
  user_id: int
  name: str


users_table: list[User] = [
  User(user_id=1, name="Joey"),
  User(user_id=2, name="Joe"),
  User(user_id=3, name="Sam"),
  User(user_id=4, name="Tim"),
  User(user_id=5, name="Ben"),
]


def get_user_id(authorization: str = Header(...)):
  token = authorization.removeprefix("Bearer ")
  try:
    return int(token)
  except ValueError:
    raise HTTPException(422, "Invalid user id.")


@app.post("/create-user", response_model=User)
def create_user(payload: UserPayload) -> User:
  new_user = User(user_id=len(users_table) + 1, name=payload.name)
  users_table.append(new_user)
  return new_user


@app.get("/me", response_model=User)
def get_user_details(user_id: int = Depends(get_user_id)):
  me = next((user for user in users_table if user.user_id == user_id), None)
  if me is None:
    raise HTTPException(404, "User doesnt exist.")
  return me
