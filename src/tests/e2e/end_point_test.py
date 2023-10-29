import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from schemas import JobInputSchema, JobSchema
from queries import user as user_queries
from queries import job as job_queries
from schemas import UserInSchema
from core import TokenGenerator

@pytest_asyncio.fixture()
async def user_access_token(real_db) -> str:
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }
    await user_queries.create(real_db, UserInSchema(**user_json))

    return TokenGenerator.create_access_token({"sub": user_json["email"]}).token

@pytest_asyncio.fixture()
async def company_access_token(real_db) -> str:
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": True
    }
    await user_queries.create(real_db, UserInSchema(**user_json))

    return TokenGenerator.create_access_token({"sub": user_json["email"]}).token
@pytest_asyncio.fixture()
async def user_refresh_token(real_db) -> str:
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }
    await user_queries.create(real_db, UserInSchema(**user_json))

    return TokenGenerator.create_refresh_token({"sub": user_json["email"]}).token




@pytest.mark.asyncio
async def test_create_job_by_company(client_app: TestClient, real_db, company_access_token):
    job_input = JobInputSchema().dict()

    response = client_app.post('/jobs',
                               headers={"Authorization": f"Bearer {company_access_token}"},
                               json=job_input)

    job = await job_queries.get_all(real_db)
    job = job[0]
    assert response.status_code == 200
    assert job.title == job_input["title"]
    assert job.description == job_input["description"]
    assert job.salary_from == job_input["salary_from"]
    assert job.salary_to == job_input["salary_to"]
    assert job.is_active == job_input["is_active"]

@pytest.mark.asyncio
async def test_create_job_by_user(client_app: TestClient, user_access_token):
    response = client_app.post('/jobs',
                               headers={"Authorization": f"Bearer {user_access_token}"},
                               json=JobInputSchema().dict())
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_refresh_token(client_app: TestClient, user_refresh_token: str):
    response = client_app.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {user_refresh_token}"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_refresh_token_by_access_token(client_app: TestClient, user_access_token: str):
    response = client_app.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
def test_create_user(client_app: TestClient):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }

    response = client_app.post(
        "/users",
        json=user_json
    )
    assert response.status_code == 200

@pytest.mark.asyncio
def test_wrong_authorize(client_app: TestClient):
    response = client_app.post(
        "/auth",
        json={
            "email": "user@example.com",
            "password": "12345678910"
        }
    )
    assert response.status_code == 401

@pytest.mark.asyncio
def test_create_user_with_incorrect_password(client_app: TestClient):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123",
        "password2": "123",
        "is_company": False
    }

    response = client_app.post(
        "/users",
        json=user_json
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_correct_login(client_app: TestClient, real_db):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }

    await user_queries.create(real_db, UserInSchema(**user_json))

    response = client_app.post(
        "/auth",
        json={
            "email": user_json["email"],
            "password": user_json["password"]
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_read_all_user(client_app: TestClient, real_db):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }

    await user_queries.create(real_db, UserInSchema(**user_json))

    response = client_app.get(
        "/users",
    )
    read_user = response.json()[0]

    assert response.status_code == 200
    assert read_user["name"] == user_json["name"]
    assert read_user["email"] == user_json["email"]
    assert read_user["is_company"] == user_json["is_company"]

@pytest.mark.asyncio
async def test_empty_jobs(client_app: TestClient):
    response = client_app.get('/jobs')
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
def test_add_jobs_by_guest(client_app):
    response = client_app.post('/jobs', json=JobInputSchema().dict())
    assert response.status_code == 403
