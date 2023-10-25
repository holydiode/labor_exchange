from typing import List

from sqlalchemy import select
from sqlalchemy_mock import AsyncSession
from models import Job
from schemas.job import JobSchema


async def create(db: AsyncSession, job_schema: JobSchema):
    new_job = Job(
        user_id=job_schema.user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
        created_at=job_schema.created_at
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    request = select(Job).limit(limit).offset(skip)
    result = await db.execute(request)
    list_of_jobs = result.fetchall()
    return list_of_jobs


async def get_by_id(db: AsyncSession, job_id: int) -> JobSchema:
    request = select(Job).where(Job.id == job_id)
    result = await db.execute(request)
    job = result.scalars().first()
    return job
