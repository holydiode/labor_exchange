import pytest
from queries import user as user_queries
from schemas import UserInSchema
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_wrong_authorize(client_app: AsyncClient):
    response = await client_app.post(
        "/auth",
        json={
            "email": "user@example.com",
            "password": "12345678910"
        }
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_refresh_token(client_app: AsyncClient, user_refresh_token: str):
    response = await client_app.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {user_refresh_token}"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_refresh_token_by_access_token(client_app: AsyncClient, user_access_token: str):
    response = await client_app.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_correct_login(client_app: AsyncClient, sa_session):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }

    await user_queries.create(sa_session, UserInSchema(**user_json))

    response = await client_app.post(
        "/auth",
        json={
            "email": user_json["email"],
            "password": user_json["password"]
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
