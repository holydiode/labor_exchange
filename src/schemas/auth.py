
from pydantic import BaseModel, EmailStr, Field


class TokenSchema(BaseModel):
    """Схема возврата токена пользователю"""
    access_token: str = Field(description="токен")
    token_type: str = Field(description="тип токена")


class LoginSchema(BaseModel):
    """Схема авторизации по email и паролю"""
    email: EmailStr = Field(default="example@mail.ru", description="почтовый адрес для авторизации")
    password: str = Field(default="123456789", description="строка пароля")
