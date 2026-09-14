import time
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


@app.middleware("http")
async def x_api_key_guard(request: Request, call_next):
  headers = request.headers

  if headers.get("x-api-key"):
    response = await call_next(request)
    return response
  else:
    return JSONResponse(status_code=400, content={"detail": "X-API-Key is missing."})


origins = ["http://amazon.com"]


app.add_middleware(
  middleware_class=CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
  start_time = time.perf_counter()
  response: Response = await call_next(request)
  end_time = time.perf_counter()
  elapsed_time = round((end_time - start_time) * 1000, 2)
  method = request.method
  path = request.url.path
  status = response.status_code
  x_req_id = request.state.x_req_id
  print(f"{method} | {path} | {status} | Time elapsed: {elapsed_time}ms | {x_req_id}")
  return response


@app.middleware("http")
async def x_request_id(request: Request, call_next):
  unique_id = uuid.uuid4()
  request.state.x_req_id = unique_id
  response: Response = await call_next(request)
  response.headers.append("X-Request-Id", str(unique_id))
  return response


@app.get("/ping")
async def get_ping(request: Request):
  return "pong"
