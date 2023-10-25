from fastapi import APIRouter, Depends, HTTPException, status
from services.responseService import response_job
from services.jobService import create_job_by_user
from schemas import JobSchema, JobInputSchema, ResponseSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries
from models import User

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
async def read_jobs(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    jobs = await job_queries.get_all(db=db, limit=limit, skip=skip)
    return jobs


@router.get("/{job_id}", response_model=JobSchema)
async def read_jobs(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await job_queries.get_by_id(db=db, job_id=job_id)
    return JobSchema.from_orm(job)


@router.post("", response_model=JobSchema)
async def create_job(job_schema: JobInputSchema,
                     db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):

    job = await create_job_by_user(db=db, job=job_schema, current_user=current_user)
    return JobSchema.from_orm(job)



@router.post("/response", response_model=ResponseSchema)
async def response(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    new_response = await response_job(db, job_id, current_user)
    return ResponseSchema.from_orm(new_response)

