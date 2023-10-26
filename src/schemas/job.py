import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class JobSchema(BaseModel):
    """Схема вакансии"""
    id: Optional[int] = Field(default=None, description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор работодателя разместившего вакансию")
    title: str = Field(default="Разработчик", description="Название вакансии")
    description: str = Field(default="", description="Описание вакансии")
    salary_from: Optional[int] = Field(default=None, description="Минимальная заработная плата")
    salary_to: Optional[int] = Field(default=None, description="Максимальная заработная плата")
    is_active: bool = Field(default=True, description="Существует ли вакансия сейчас")
    created_at: datetime.datetime = Field(default=datetime.datetime.utcnow(), description="Название вакансии")

    class Config:
        orm_mode = True


class JobInputSchema(BaseModel):
    """Схема используемая для создания новой вакансии для работодателя"""
    title: str = Field(default="Разработчик", description="Название вакансии")
    description: str = Field(default="", description="Описание вакансии")
    salary_from: Optional[int] = Field(default=None, description="Минимальная заработная плата")
    salary_to: Optional[int] = Field(default=None, description="Максимальная заработная плата")
    is_active: bool = Field(default=True, description="Существует ли вакансия сейчас")

    @classmethod
    @validator("salary_to")
    def password_match(cls, v, values, **kwargs):
        salary_from = values['salary_from']
        if v is not None and salary_from is not None and v < values['salary_from']:
            raise ValueError("Максимальная зарплата не может быть меньше минимальной")
        return True
