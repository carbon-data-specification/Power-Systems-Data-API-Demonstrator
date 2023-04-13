# SPDX-License-Identifier: Apache-2.0

from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from power_systems_data_api_demonstrator.seed.seed import seed_data
from power_systems_data_api_demonstrator.settings import settings
from power_systems_data_api_demonstrator.src.application import get_app
from power_systems_data_api_demonstrator.src.lib.db.dependencies import (
    get_db_session,
    init_session,
)
from power_systems_data_api_demonstrator.src.lib.db.meta import meta  # noqa: WPS433
from power_systems_data_api_demonstrator.src.lib.db.models import (  # noqa: WPS433
    load_all_models,
)
from power_systems_data_api_demonstrator.src.lib.db.utils import (
    create_database,
    drop_database,
)


@pytest.fixture
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.
    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.
    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        await init_session(session)
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(dbsession: AsyncSession) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331


@pytest.fixture
async def fastapi_client(
    fastapi_app: FastAPI, dbsession: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    await seed_data(dbsession)
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
