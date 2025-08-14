import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from source.config import app_config
from source.core.enum import SubscriptionType, UserType
from source.core.schemas.user_schema import UserSchema
from source.infrastructure.database.repository.user_repo import UserRepository


# Фикстура для event loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    test_db_url = app_config.DATABASE_URL

    test_engine = create_async_engine(
        test_db_url,
        echo=True,
        poolclass=NullPool,  # Используем NullPool для тестов
    )

    yield test_engine

    await test_engine.dispose()


@pytest.fixture
async def session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker(
            test_engine,
            expire_on_commit=False,
            autoflush=False
    )() as test_session:
        try:
            yield test_session
        finally:
            await test_session.rollback()

            # Очищаем все таблицы. Важно.
            async with test_engine.begin() as conn:
                await conn.run_sync(lambda sync_conn: sync_conn.execute(text("TRUNCATE TABLE users CASCADE")))

            await test_session.close()


@pytest.fixture(scope="function")
async def user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session=session)


@pytest.fixture
async def user_schema() -> UserSchema:
    return UserSchema(
        telegram_id="1488",
        username="sperma",
        dialogs_completed=0,
        user_type=UserType.USER,
        subscription=SubscriptionType.FREE
    )