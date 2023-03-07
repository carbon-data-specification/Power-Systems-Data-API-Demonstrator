import asyncio
import os
import pandas as pd
from power_systems_data_api_demonstrator.src.lib.db.dao.grid_node_dao import GridNodeDAO
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GridNodeModel,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from power_systems_data_api_demonstrator.src.lib.db.base import Base
from power_systems_data_api_demonstrator.settings import Settings
from power_systems_data_api_demonstrator.src.api.grid_node.schema import GridNodeType

DATA_DIR = "data"

AVAILABLE_ENTITIES = ["EIA", "ENTSO-E"]  # os.listdir(DATA_DIR)


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
        grid_node_service = GridNodeDAO(session)
        for entity in AVAILABLE_ENTITIES:
            df_generation = pd.read_csv(
                os.path.join(DATA_DIR, entity, "generation.csv")
            )
            for balancing_region in df_generation["Balancing Region"].unique():
                id_ = f"{entity}-{balancing_region}"
                await grid_node_service.create_grid_node(
                    GridNodeModel(id=id_, name=id_, type=GridNodeType.SYSTEM)
                )

                df_ba = df_generation[
                    df_generation["Balancing Region"] == balancing_region
                ].copy()

            df_io = pd.read_csv(os.path.join(DATA_DIR, entity, "imports_exports.csv"))
            df_capacity = pd.read_csv(
                os.path.join(DATA_DIR, entity, "installed_capacity.csv")
            )

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
