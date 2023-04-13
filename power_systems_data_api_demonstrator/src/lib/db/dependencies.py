# SPDX-License-Identifier: Apache-2.0

from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        await init_session(session)
        yield session
    finally:
        await session.commit()
        await session.close()


async def init_session(session: AsyncSession) -> None:
    await session.execute(text("PRAGMA foreign_keys = ON"))
    await session.commit()
