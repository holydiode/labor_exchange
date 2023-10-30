from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Response
from schemas import ResponseSchema


async def create(db: AsyncSession, response: ResponseSchema) -> Response:
    new_response = Response(
        job_id=response.job_id,
        user_id=response.user_id,
        message=response.message
    )
    db.add(new_response)
    await db.commit()
    await db.refresh(new_response)
    return new_response


async def get_by_user_id(db: AsyncSession, user_id: int) -> List[Response]:
    request = select(Response).where(Response.user_id == user_id)
    result = await db.execute(request)
    list_of_responses = result.scalars().all()
    return list_of_responses
