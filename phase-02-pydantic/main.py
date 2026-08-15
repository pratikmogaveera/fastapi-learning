from fastapi import FastAPI

app = FastAPI()

# EXERCISE 1 — Basic request + response models
# Define:
#   CreateLinkRequest: original_url (str), custom_slug (str | None = None)
#   LinkResponse: id (int), short_code (str), original_url (str)
#
# Create POST /links that accepts CreateLinkRequest body and returns a fake LinkResponse
# (hardcode the response for now, no DB)

# TODO: implement here


# EXERCISE 2 — Field validation
# Add the following validation to CreateLinkRequest:
#   - original_url must be a valid URL (use AnyHttpUrl from pydantic or a validator)
#   - custom_slug, if provided, must be 3-20 chars, alphanumeric + hyphens only (use regex)
#
# Test: POST with original_url="not-a-url" → 422 with clear error
# Test: POST with custom_slug="ab" → 422 (too short)

# TODO: update your model here


# EXERCISE 3 — model_validator (cross-field validation)
# Add a model_validator to CreateLinkRequest that:
#   - If custom_slug is provided, checks that it doesn't contain the word "admin"
#   - Raises ValueError if it does
#
# Hint: use @model_validator(mode='after') from pydantic

# TODO: implement here


# EXERCISE 4 — Nested models
# Define an Address model: street (str), city (str), country (str)
# Define a CreateUserRequest: name (str), email (str), address (Address)
# Create POST /users that accepts it and echoes it back
# Test with nested JSON body

# TODO: implement here
