import pytest

from dependencies.user import get_token_owner
from models import Response
from queries import user as user_queries
from schemas import UserInSchema, JobSchema, ResponseSchema
from httpx import AsyncClient
from queries import job as job_queries
from queries import response as response_queries


@pytest.mark.asyncio
async def test_create_user(client_app: AsyncClient):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }

    response = await client_app.post(
        "/users",
        json=user_json
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user_with_incorrect_password(client_app: AsyncClient):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123",
        "password2": "123",
        "is_company": False
    }

    response = await client_app.post(
        "/users",
        json=user_json
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_all_user(client_app: AsyncClient, sa_session):
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }

    await user_queries.create(sa_session, UserInSchema(**user_json))

    response = await client_app.get(
        "/users",
    )
    read_user = response.json()[0]

    assert response.status_code == 200
    assert read_user["name"] == user_json["name"]
    assert read_user["email"] == user_json["email"]
    assert read_user["is_company"] == user_json["is_company"]


@pytest.mark.asyncio
async def test_update(client_app: AsyncClient, company_access_token: str, sa_session):
    user = await get_token_owner(sa_session, company_access_token, "access")

    changing_json = {
        "name": "chg",
        "email": "chg@example.com",
        "is_company": False
    }
    response = await client_app.put(
        f'/users',
        headers={"Authorization": f"Bearer {company_access_token}"},
        json=changing_json
    )

    assert response.status_code == 200
    assert changing_json["name"] == user.name
    assert changing_json["email"] == user.email
    assert changing_json["is_company"] == user.is_company


@pytest.mark.asyncio
async def test_update(client_app: AsyncClient, company_access_token: str, sa_session):
    user = await get_token_owner(sa_session, company_access_token, "access")

    changing_json = {
        "name": "chg",
        "email": "chg@example.com",
        "is_company": False
    }
    response = await client_app.put(
        f'/users',
        headers={"Authorization": f"Bearer {company_access_token}"},
        json=changing_json
    )

    assert response.status_code == 200
    assert changing_json["name"] == user.name
    assert changing_json["email"] == user.email
    assert changing_json["is_company"] == user.is_company


@pytest.mark.asyncio
async def test_read_responses_by_user(client_app: AsyncClient, user_access_token: str, sa_session):
    user = await get_token_owner(sa_session, user_access_token, "access")
    added_job = await job_queries.create(sa_session, JobSchema(user_id=user.id))
    await response_queries.create(sa_session, ResponseSchema(user_id=user.id, job_id=added_job.id))

    response = await client_app.get(
        f'/users/{user.id}/responses',
        headers={"Authorization": f"Bearer {user_access_token}"}
    )

    assert response.status_code == 200
    assert response.json()[0]["user_id"] == user.id
    assert response.json()[0]["job_id"] == added_job.id


@pytest.mark.asyncio
async def test_read_responses_by_company(client_app: AsyncClient,
                                         user_access_token: str,
                                         company_access_token: str,
                                         sa_session):
    user = await get_token_owner(sa_session, user_access_token, "access")
    company = await get_token_owner(sa_session, company_access_token, "access")
    added_job = await job_queries.create(sa_session, JobSchema(user_id=company.id))
    await response_queries.create(sa_session, ResponseSchema(user_id=user.id, job_id=added_job.id))

    response = await client_app.get(
        f'/users/{user.id}/responses',
        headers={"Authorization": f"Bearer {company_access_token}"}
    )

    assert response.status_code == 200
    assert response.json()[0]["user_id"] == user.id
    assert response.json()[0]["job_id"] == added_job.id

@pytest.mark.asyncio
async def test_read_responses_by_company(client_app: AsyncClient,
                                         user_access_token: str,
                                         company_access_token: str,
                                         sa_session):
    user = await get_token_owner(sa_session, user_access_token, "access")
    added_job = await job_queries.create(sa_session, JobSchema(user_id=user.id))
    await response_queries.create(sa_session, ResponseSchema(user_id=user.id, job_id=added_job.id))

    response = await client_app.get(
        f'/users/{user.id}/responses',
        headers={"Authorization": f"Bearer {company_access_token}"}
    )

    assert response.status_code == 200
    assert response.json() == []