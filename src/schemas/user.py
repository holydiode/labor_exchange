import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None


class UserInSchema(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @field_validator("password2")
    def password_match(cls, v: str, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data["password"]:
            raise ValueError("Пароли не совпадают!")
        return v
