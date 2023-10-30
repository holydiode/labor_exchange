import pytest
from schemas import JobInputSchema, JobSchema
from queries import user as user_queries
from queries import job as job_queries
from schemas import UserInSchema
from httpx import AsyncClient
from dependencies.user import get_token_owner


@pytest.mark.asyncio
async def test_create_job_by_company(client_app: AsyncClient, sa_session, company_access_token):
    job_input = JobInputSchema().dict()

    response = await client_app.post('/jobs',
                                     headers={"Authorization": f"Bearer {company_access_token}"},
                                     json=job_input)

    job = await job_queries.get_all(sa_session)
    job = job[0]
    assert response.status_code == 200
    assert job.title == job_input["title"]
    assert job.description == job_input["description"]
    assert job.salary_from == job_input["salary_from"]
    assert job.salary_to == job_input["salary_to"]
    assert job.is_active == job_input["is_active"]


@pytest.mark.asyncio
async def test_create_job_by_user(client_app: AsyncClient, user_access_token):
    response = await client_app.post('/jobs',
                                     headers={"Authorization": f"Bearer {user_access_token}"},
                                     json=JobInputSchema().dict())
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_add_jobs_by_guest(client_app: AsyncClient):
    response = await client_app.post('/jobs', json=JobInputSchema().dict())
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_job_by_id(client_app: AsyncClient, company_access_token: str, sa_session):
    user = await get_token_owner(sa_session, company_access_token, "access")
    added_job = await job_queries.create(sa_session, JobSchema(user_id=user.id))

    response = await client_app.get(
        f'/jobs/{added_job.id}'
    )

    assert response.status_code == 200
    assert added_job.user_id == response.json()["user_id"]
    assert added_job.title == response.json()["title"]
    assert added_job.description == response.json()["description"]
    assert added_job.salary_from == response.json()["salary_from"]
    assert added_job.salary_to == response.json()["salary_to"]
    assert added_job.is_active == response.json()["is_active"]


@pytest.mark.asyncio
async def test_read_not_existed_job_by_id(client_app: AsyncClient, sa_session):
    response = await client_app.get(
        f'/jobs/-1'
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_response_jobby_user(client_app: AsyncClient, user_access_token: str, sa_session):
    user = await get_token_owner(sa_session, user_access_token, "access")
    added_job = await job_queries.create(sa_session, JobSchema(user_id=user.id))

    response = await client_app.post(
        f'/jobs/{added_job.id}/response',
        headers={"Authorization": f"Bearer {user_access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == user.id
    assert response.json()["job_id"] == user.id


@pytest.mark.asyncio
async def test_response_jobby_company(client_app: AsyncClient, company_access_token: str, sa_session):
    user = await get_token_owner(sa_session, company_access_token, "access")
    added_job = await job_queries.create(sa_session, JobSchema(user_id=user.id))

    response = await client_app.post(
        f'/jobs/{added_job.id}/response',
        headers={"Authorization": f"Bearer {company_access_token}"}
    )

    assert response.status_code == 403
