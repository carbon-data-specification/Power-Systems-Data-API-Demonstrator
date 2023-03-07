import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from power_systems_data_api_demonstrator.settings import Settings
from power_systems_data_api_demonstrator.src.lib.db.base import Base
from power_systems_data_api_demonstrator.src.lib.db.dao.grid_node_dao import GridNodeDAO
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GridNodeModel,
)


async def async_main() -> None:
    settings = Settings()
    engine = create_async_engine(
        settings.db_url,
        echo=True,
    )

    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        grid_node_service = GridNodeDAO(session)
        await grid_node_service.create_grid_node(
            GridNodeModel(id="ABC", name="DEF", type="GHI")
        )

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
