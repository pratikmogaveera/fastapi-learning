# Python Basics for FastAPI
# Run this file: python exercises.py
# Complete each exercise, then run to verify your output matches the expected output shown in comments.

# ─────────────────────────────────────────────
# EXERCISE 1 — Type Hints
# ─────────────────────────────────────────────
# FastAPI uses type hints everywhere. This is how Python knows what type a parameter is.
#
# Read: https://docs.python.org/3/library/typing.html (just the first screen)
#
# Task: Fix the function below so it has correct type hints.
# - `name` should be a str
# - `age` should be an int
# - return type should be str
# - `email` should be optional (can be str or None), default None
#
# Expected output:
# Hello Pratik, age 26
# Hello Pratik, age 26, email: pratik@example.com

from typing import Optional

def greet(name, age, email=None):  # add type hints here
    if email:
        return f"Hello {name}, age {age}, email: {email}"
    return f"Hello {name}, age {age}"

print(greet("Pratik", 26))
print(greet("Pratik", 26, "pratik@example.com"))


# ─────────────────────────────────────────────
# EXERCISE 2 — Classes and __init__
# ─────────────────────────────────────────────
# Pydantic models are classes. You need to understand basic class syntax.
#
# Task: Create a class `Link` with:
# - __init__ that accepts: short_code (str), original_url (str), click_count (int = 0)
# - A method `increment_clicks()` that adds 1 to click_count
# - A method `to_dict()` that returns {"short_code": ..., "original_url": ..., "click_count": ...}
#
# Expected output:
# {'short_code': 'abc123', 'original_url': 'https://google.com', 'click_count': 0}
# {'short_code': 'abc123', 'original_url': 'https://google.com', 'click_count': 3}

# TODO: define class Link here

link = Link("abc123", "https://google.com")
print(link.to_dict())
link.increment_clicks()
link.increment_clicks()
link.increment_clicks()
print(link.to_dict())


# ─────────────────────────────────────────────
# EXERCISE 3 — Decorators
# ─────────────────────────────────────────────
# @app.get("/path") is a decorator. Understanding decorators removes the magic.
#
# Task: Create a decorator `log_call` that:
# - Prints "Calling: <function name>" before the function runs
# - Prints "Done: <function name>" after it runs
# - Returns the function's return value unchanged
#
# Then apply it to a function `get_user()` that returns {"id": 1, "name": "Pratik"}
#
# Expected output:
# Calling: get_user
# Done: get_user
# {'id': 1, 'name': 'Pratik'}
#
# Hint: a decorator is a function that takes a function and returns a function.
# def log_call(func):
#     def wrapper(*args, **kwargs):
#         ...
#     return wrapper

# TODO: implement log_call decorator

# TODO: apply decorator to get_user and call it
result = get_user()
print(result)


# ─────────────────────────────────────────────
# EXERCISE 4 — async / await
# ─────────────────────────────────────────────
# FastAPI is async. Every route handler can be async. DB calls must be awaited.
#
# Read: https://docs.python.org/3/library/asyncio-task.html (just the "Coroutines" section)
#
# Task:
# 1. Write an async function `fetch_link(short_code: str)` that:
#    - Simulates a DB call with `await asyncio.sleep(0.1)`
#    - Returns {"short_code": short_code, "url": "https://example.com"}
#
# 2. Write an async function `main()` that:
#    - Calls fetch_link("abc123") and stores the result
#    - Prints the result
#
# 3. Run it with asyncio.run(main())
#
# Expected output:
# {'short_code': 'abc123', 'url': 'https://example.com'}

import asyncio

# TODO: implement fetch_link and main


# ─────────────────────────────────────────────
# EXERCISE 5 — *args and **kwargs
# ─────────────────────────────────────────────
# FastAPI's Depends() and decorators pass arguments around using these.
# You won't write them often but you need to read them without confusion.
#
# Task: implement a function `describe(**kwargs)` that:
# - Accepts any keyword arguments
# - Prints each key-value pair as "key: value"
#
# Then call: describe(name="Pratik", role="SDE1", company="MO")
#
# Expected output:
# name: Pratik
# role: SDE1
# company: MO

# TODO: implement describe


# ─────────────────────────────────────────────
# EXERCISE 6 — List and Dict comprehensions
# ─────────────────────────────────────────────
# Used constantly when shaping API responses and filtering data.
#
# Task A: Given this list of links, use a list comprehension to get only active links' short_codes
# Expected: ['abc', 'xyz']
#
# Task B: Use a dict comprehension to build {short_code: original_url} from active links only
# Expected: {'abc': 'https://google.com', 'xyz': 'https://github.com'}

links = [
    {"short_code": "abc", "original_url": "https://google.com", "is_active": True},
    {"short_code": "def", "original_url": "https://deleted.com", "is_active": False},
    {"short_code": "xyz", "original_url": "https://github.com", "is_active": True},
]

# TODO: Task A — list comprehension

# TODO: Task B — dict comprehension
