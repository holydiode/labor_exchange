from typing import List

from starlette import status

import queries.response
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Response, User
import queries.job as job_query
import queries.response as response_query
from schemas import ResponseSchema


async def response_job(db: AsyncSession, job_id: int, current_user: User) -> Response:
    job = await job_query.get_by_id(db, job_id)

    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user can't create job")
    if job is None or not job.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found or disable")

    response = await queries.response.create(db, ResponseSchema(job_id=job.id, user_id=current_user.id, message=""))
    return response


async def get_all_accessible_response_of_user(db: AsyncSession, user_id: int, current_user: User) -> List[Response]:
    if not current_user.is_company and user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user can get only onw response")
    responses = await response_query.get_by_user_id(db, user_id)
    if current_user.is_company:
        responses = [response for response in responses if response.job.user_id == current_user.id]
    return responses
