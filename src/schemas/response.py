from typing import Optional

from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """Схема отклика работника на вакансию"""
    id: Optional[int] = Field(default=None, description="Идентификатор отклика")
    user_id: int = Field(description="Идентификатор работника, откликнувшегося на вакансию")
    job_id: int = Field(description="Идентификатор вакансии")
    message: str = Field(default="", description="Сопроводительное письмо")

    class Config:
        orm_mode = True
