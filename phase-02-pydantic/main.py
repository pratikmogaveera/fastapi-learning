from fastapi import FastAPI
from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, model_validator

app = FastAPI()

# EXERCISE 1 — Basic request + response models
# Define:
#   CreateLinkRequest: original_url (str), custom_slug (str | None = None)
#   LinkResponse: id (int), short_code (str), original_url (str)
#
# Create POST /links that accepts CreateLinkRequest body and returns a fake LinkResponse
# (hardcode the response for now, no DB)


class CreateLinkRequestBasic(BaseModel):
    original_url: str
    custom_slug: str | None = None


class LinkResponseBasic(BaseModel):
    id: int
    short_code: str
    original_url: str


@app.post("/links-basic", response_model=LinkResponseBasic)
async def create_links_basic(payload: CreateLinkRequestBasic):
    return {"id": 1, "short_code": "xna6", "original_url": payload.original_url}


# EXERCISE 2 — Field validation
# Add the following validation to CreateLinkRequest:
#   - original_url must be a valid URL (use AnyHttpUrl from pydantic or a validator)
#   - custom_slug, if provided, must be 3-20 chars, alphanumeric + hyphens only (use regex)
#
# Test: POST with original_url="not-a-url" → 422 with clear error
# Test: POST with custom_slug="ab" → 422 (too short)


# EXERCISE 3 — model_validator (cross-field validation)
# Add a model_validator to CreateLinkRequest that:
#   - If custom_slug is provided, checks that it doesn't contain the word "admin"
#   - Raises ValueError if it does
#
# Hint: use @model_validator(mode='after') from pydantic


class CreateLinkRequest(BaseModel):
    # Ex 2 — AnyHttpUrl validates the URL format
    original_url: AnyHttpUrl
    # Ex 2 — Field constraints: 3-20 chars, alphanumeric + hyphens only
    custom_slug: str | None = Field(
        default=None, min_length=3, max_length=20, pattern="^[-a-z0-9]+$"
    )

    # Ex 3 — cross-field validation: slug must not contain "admin"
    @model_validator(mode="after")
    def verify_slug(self):
        if self.custom_slug and "admin" in self.custom_slug:
            raise ValueError("Slug must not contain 'admin'.")
        return self


class LinkResponse(BaseModel):
    id: int
    short_code: str
    original_url: AnyHttpUrl


@app.post("/links", response_model=LinkResponse)
async def create_links(payload: CreateLinkRequest):
    return {"id": 1, "short_code": "xna6", "original_url": payload.original_url}


# EXERCISE 4 — Nested models
# Define an Address model: street (str), city (str), country (str)
# Define a CreateUserRequest: name (str), email (str), address (Address)
# Create POST /users that accepts it and echoes it back
# Test with nested JSON body


class Address(BaseModel):
    street: str
    city: str
    country: str


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    address: Address


class CreateUserResponse(BaseModel):
    name: str
    email: EmailStr
    address: Address


@app.post("/user", response_model=CreateUserResponse)
async def create_user(payload: CreateUserRequest):
    return payload
