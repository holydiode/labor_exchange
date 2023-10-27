from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_token
from queries import user as user_queries
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db
from models import User


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials are not valid")
    payload = decode_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    token_type: str = payload.get("token_type")
    if token_type is None or token_type != "access":
        raise cred_exception
    if email is None:
        raise cred_exception
    user = await user_queries.get_by_email(db=db, email=email)
    if user is None:
        raise cred_exception
    return user


async def refresh_user(db: AsyncSession = Depends(get_db), token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials are not valid")
    payload = decode_token(token)
    if payload is None:
        raise cred_exception
    token_type: str = payload.get("token_type")
    email: str = payload.get("sub")

    if token_type is None or token_type != "refresh":
        raise cred_exception
    if email is None:
        raise cred_exception

    user = await user_queries.get_by_email(db=db, email=email)
    if user is None:
        raise cred_exception
    return user
