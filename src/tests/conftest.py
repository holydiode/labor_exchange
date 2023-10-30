import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core import TokenGenerator
from dependencies import get_db
from fixtures.users import UserFactory
from fastapi.testclient import TestClient
from main import app
import pytest_asyncio
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL
from schemas import UserInSchema
from queries import user as user_queries


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    async def mock_delete(instance):
        session.expunge(instance)
        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


@pytest_asyncio.fixture()
async def client_app(sa_session: AsyncSession) -> AsyncClient:
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session


@pytest_asyncio.fixture()
async def user_access_token(sa_session) -> str:
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }
    await user_queries.create(sa_session, UserInSchema(**user_json))

    return TokenGenerator.create_access_token({"sub": user_json["email"]}).token
@pytest_asyncio.fixture()
async def company_access_token(sa_session) -> str:
    user_json = {
        "name": "user",
        "email": "company@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": True
    }
    await user_queries.create(sa_session, UserInSchema(**user_json))

    return TokenGenerator.create_access_token({"sub": user_json["email"]}).token
@pytest_asyncio.fixture()
async def user_refresh_token(sa_session) -> str:
    user_json = {
        "name": "user",
        "email": "user@example.com",
        "password": "123456789",
        "password2": "123456789",
        "is_company": False
    }
    await user_queries.create(sa_session, UserInSchema(**user_json))

    return TokenGenerator.create_refresh_token({"sub": user_json["email"]}).token

