from starlette import status

import queries.response
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import  Response, User
from queries.job import get_by_id
from schemas import ResponseSchema


async def response_job(db: AsyncSession, job_id: int, current_user: User) -> Response:
    job = await get_by_id(db, job_id)

    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user can't create job")
    if not job.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found or disable")

    response = await queries.response.create(db, ResponseSchema(job_id=job.id, user_id=current_user.id, message=""))
    return response
