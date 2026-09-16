import pytest_asyncio
from httpx import ASGITransport, AsyncClient, Response
from main import app, get_user_id


async def get_mock_user_id():
  return 1


@pytest_asyncio.fixture
async def client():
  client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
  yield client
  await client.aclose()


async def test_create_user_success(client):
  payload = {"name": "Joey"}
  response: Response = await client.post(url="/create-user", json=payload)

  assert response.status_code == 200
  assert type(response.json()["user_id"]) is int
  assert response.json()["name"] == payload["name"]


async def test_create_user_missing_required_field(client):
  payload = {}
  response: Response = await client.post(url="/create-user", json=payload)

  assert response.status_code == 422


async def test_create_user_invalid_field_type(client):
  payload = {"name": 1}
  response: Response = await client.post(url="/create-user", json=payload)

  assert response.status_code == 422


async def test_get_me_returns_user(client: AsyncClient):
  response: Response = await client.get(url="/me", headers={"Authorization": "Bearer 1"})

  assert response.status_code == 200
  assert type(response.json()["user_id"]) is int
  assert type(response.json()["name"]) is str


async def test_get_me_missing_auth_header(client: AsyncClient):
  response: Response = await client.get(url="/me")

  assert response.status_code == 422


async def test_get_me_user_not_found(client: AsyncClient):
  response: Response = await client.get(url="/me", headers={"Authorization": "Bearer 100"})

  assert response.status_code == 404


async def test_get_me_with_mocked_dependency(client: AsyncClient):
  try:
    app.dependency_overrides[get_user_id] = get_mock_user_id
    response: Response = await client.get(url="/me")

    assert response.status_code == 200
    assert type(response.json()["user_id"]) is int
    assert type(response.json()["name"]) is str
    assert response.json()["user_id"] == 1
  finally:
    app.dependency_overrides.clear()
