import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_flakewatch.db"

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from flakewatch.main import app
from flakewatch.models import Base
from flakewatch.database import engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def client(setup_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
