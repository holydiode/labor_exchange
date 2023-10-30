from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.user import get_refreshed_user
from models import User
from queries import user as user_queries

from schemas import TokenSchema, LoginSchema, PairTokenSchema
from core.security import verify_password
from dependencies import get_db
from core import TokenGenerator

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=PairTokenSchema)
async def login(login: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректное имя пользователя или пароль")

    return PairTokenSchema(
        access_token=TokenGenerator.create_access_token({"sub": user.email}),
        refresh_token=TokenGenerator.create_refresh_token({"sub": user.email}),
    )


@router.post("/refresh", response_model=PairTokenSchema)
async def auth_with_refresh_token(current_user: User = Depends(get_refreshed_user)):
    return PairTokenSchema(
        access_token=TokenGenerator.create_access_token({"sub": current_user.email}),
        refresh_token=TokenGenerator.create_refresh_token({"sub": current_user.email}),
    )
