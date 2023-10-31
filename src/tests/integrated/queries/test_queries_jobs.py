import pytest
from sqlalchemy import select

from fixtures.jobs import JobFactory
from queries import job as job_query
from fixtures.users import UserFactory
from models import Job
from schemas import JobSchema


@pytest.mark.asyncio
async def test_get_all_with_empty(sa_session):
    jobs = await job_query.get_all(sa_session)
    assert jobs == []


@pytest.mark.asyncio
async def test_get_all(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()
    jobs = await job_query.get_all(sa_session)

    assert jobs
    assert len(jobs) == 1
    assert jobs[0] == job


@pytest.mark.asyncio
async def test_get_by_id(sa_session):
    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    request = select(Job).limit(1)
    bd_job = await sa_session.scalar(request)

    find_job = await job_query.get_by_id(sa_session, bd_job.id)
    assert find_job
    assert find_job == job


@pytest.mark.asyncio
async def test_get_by_missmatch_id(sa_session):
    job_in_bd = await job_query.get_by_id(sa_session, -1)
    assert job_in_bd is None


@pytest.mark.asyncio
async def test_create(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    added_job = await job_query.create(sa_session, JobSchema(user_id=user.id))

    request = select(Job).where(added_job.id == Job.id)
    bd_job = await sa_session.scalar(request)

    assert bd_job
    assert bd_job == added_job
