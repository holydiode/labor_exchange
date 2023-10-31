from datetime import datetime

from fastapi import HTTPException
from sqlalchemy_mock import AsyncSession
from starlette import status

from models import User, Job
from schemas import JobInputSchema, JobSchema
import queries.job as job_query


async def create_job_by_user(db: AsyncSession, job: JobInputSchema, current_user: User) -> Job:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user can't create job")

    new_job = JobSchema(**job.model_dump(), user_id=current_user.id, created_at=datetime.utcnow())
    return await job_query.create(db=db, job_schema=new_job)
