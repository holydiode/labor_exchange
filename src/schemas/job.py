import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobInputSchema(BaseModel):
    title: str = Field(default="Разработчик", description="Название вакансии")
    description: str = Field(default="", description="Описание вакансии")
    salary_from: Optional[int] = Field(default=None, description="Минимальная заработная плата")
    salary_to: Optional[int] = Field(default=None, description="Максимальная заработная плата")
    is_active: bool = Field(default=True, description="Существует ли вакансия сейчас")
