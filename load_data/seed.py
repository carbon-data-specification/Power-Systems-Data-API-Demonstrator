import asyncio
import logging
import os

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from power_systems_data_api_demonstrator.settings import Settings
from power_systems_data_api_demonstrator.src.api.grid_node.schema import (
    FuelTypes,
    GridNodeType,
)
from power_systems_data_api_demonstrator.src.lib.config import GRID_NODES
from power_systems_data_api_demonstrator.src.lib.db.base import Base
from power_systems_data_api_demonstrator.src.lib.db.dao.fuel_type_dao import FuelTypeDAO
from power_systems_data_api_demonstrator.src.lib.db.dao.grid_node_dao import GridNodeDAO
from power_systems_data_api_demonstrator.src.lib.db.models.fuel_types import (
    FuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GridNodeModel,
)

logger = logging.getLogger(__name__)

DATA_DIR = "data"


def get_grid_node_by_id(grid_node_id: str) -> dict:
    return next(
        grid_node for grid_node in GRID_NODES if grid_node.get("id") == grid_node_id
    )


async def seed_fuel_types(session: AsyncSession) -> None:
    fuel_type_service = FuelTypeDAO(session)
    for fuel_type in FuelTypes:
        await fuel_type_service.create_fuel_type(FuelTypeModel(name=fuel_type))
    pass


async def seed_grid_nodes(session: AsyncSession) -> None:
    grid_node_service = GridNodeDAO(session)
    for source in set([grid_node.get("source") for grid_node in GRID_NODES]):
        try:
            df_generation = pd.read_csv(
                os.path.join(DATA_DIR, source, "generation.csv")
            )
            for grid_node_id in df_generation["Grid Node"].unique():
                id_ = grid_node_id.upper()
                assert id_ in [grid_node.get("id") for grid_node in GRID_NODES]
                g_n = get_grid_node_by_id(id_)
                await grid_node_service.create_grid_node(
                    GridNodeModel(
                        id=g_n.get("id"), name=g_n.get("g_n"), type=g_n.get("type")
                    )
                )
        except FileNotFoundError:
            logger.error(f"Could not find generation.csv for {source}")
            continue


async def seed_generation(session: AsyncSession) -> None:
    # TODO
    pass


async def async_main() -> None:
    settings = Settings()
    engine = create_async_engine(
        str(settings.db_url),
        echo=True,
    )

    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await seed_fuel_types(session)
        await seed_grid_nodes(session)
        await seed_generation(session)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
