import asyncio
import functools
import logging
import os
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any, ParamSpec, TypeVar

import click
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from power_systems_data_api_demonstrator.settings import Settings
from power_systems_data_api_demonstrator.src.api.grid_node.schema import FuelTypes
from power_systems_data_api_demonstrator.src.lib.config import GRID_NODES
from power_systems_data_api_demonstrator.src.lib.db.base import Base
from power_systems_data_api_demonstrator.src.lib.db.dao.fuel_type_dao import FuelTypeDAO
from power_systems_data_api_demonstrator.src.lib.db.dao.grid_node_dao import GridNodeDAO
from power_systems_data_api_demonstrator.src.lib.db.models.exchanges import (
    ExchangeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.fuel_types import (
    FuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.generation import (
    GenerationForFuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GridNodeModel,
)

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
AVAILABLE_DATA_SOURCES = os.listdir(DATA_DIR)


def get_grid_node_by_id(grid_node_id: str) -> dict[str, Any]:
    return next(
        grid_node for grid_node in GRID_NODES if grid_node.get("id") == grid_node_id
    )


async def seed_fuel_types(session: AsyncSession) -> None:
    fuel_type_service = FuelTypeDAO(session)
    for fuel_type in FuelTypes:
        await fuel_type_service.create_fuel_type(FuelTypeModel(name=fuel_type))


async def seed_grid_nodes(
    session: AsyncSession, /, *, grid_node_sources: list[str]
) -> None:
    grid_node_service = GridNodeDAO(session)
    for source in grid_node_sources:
        try:
            df_exchanges = pd.read_csv(
                os.path.join(DATA_DIR, source, "imports_exports.csv")
            )
            all_grid_node_ids = set(df_exchanges["Grid Node To"].unique()).union(
                set(df_exchanges["Grid Node From"].unique())
            )
            for grid_node_id in all_grid_node_ids:
                id_ = grid_node_id.upper()
                assert id_ in [
                    grid_node.get("id") for grid_node in GRID_NODES
                ], f"{id_} not in GRID_NODES"
                g_n = get_grid_node_by_id(id_)
                await grid_node_service.create_grid_node(
                    GridNodeModel(
                        id=g_n.get("id"), name=g_n.get("name"), type=g_n.get("type")
                    )
                )

        except FileNotFoundError:
            logger.error(f"Could not find generation.csv for {source}")
            continue


async def seed_generation(
    session: AsyncSession, /, *, grid_node_sources: list[str]
) -> None:
    grid_node_service = GridNodeDAO(session)
    for source in grid_node_sources:
        try:
            df_generation = pd.read_csv(
                os.path.join(DATA_DIR, source, "generation.csv")
            )
            for grid_node_id in df_generation["Grid Node"].unique():
                df_this_nodes_generation = df_generation[
                    df_generation["Grid Node"] == grid_node_id
                ]
                df_generation_rows = pd.melt(
                    df_this_nodes_generation,
                    id_vars=["Grid Node", "datetime", "unit"],
                    var_name="fuel_type",
                    value_name="value",
                ).reset_index()

                await grid_node_service.add_generation_for_fuel_type(
                    [
                        GenerationForFuelTypeModel(
                            datetime=pd.to_datetime(row["datetime"]),
                            value=row["value"],
                            fuel_type=row["fuel_type"],
                            unit=row["unit"],
                            grid_node_id=grid_node_id,
                        )
                        for i, row in df_generation_rows.iterrows()
                    ]
                )

        except FileNotFoundError:
            logger.error(f"Could not find generation.csv for {source}")
            continue


async def seed_exchanges(
    session: AsyncSession, /, *, grid_node_sources: list[str]
) -> None:
    grid_node_service = GridNodeDAO(session)
    for source in grid_node_sources:
        try:
            df_exchanges = pd.read_csv(
                os.path.join(DATA_DIR, source, "imports_exports.csv")
            )

            await grid_node_service.add_exchanges(
                [
                    ExchangeModel(
                        datetime=pd.to_datetime(row["datetime"]),
                        value=row["Value"],
                        unit=row["unit"],
                        grid_node_from_id=row["Grid Node From"],
                        grid_node_to_id=row["Grid Node To"],
                    )
                    for i, row in df_exchanges.iterrows()
                ]
            )

        except FileNotFoundError:
            logger.error(f"Could not find imports_exports.csv for {source}")
            continue


def make_sync(func: Callable[P, Awaitable[T]]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        return asyncio.run(func(*args, **kwargs))  # type: ignore

    return wrapper


async def seed_data(
    session: AsyncSession, grid_node_sources: list[str] | None = None
) -> None:
    grid_node_sources = grid_node_sources or sorted(
        set(
            [
                grid_node.get("source")
                for grid_node in GRID_NODES
                if grid_node.get("source")
            ]
        )
    )
    await seed_fuel_types(session)
    await seed_grid_nodes(session, grid_node_sources=grid_node_sources)
    await seed_generation(session, grid_node_sources=grid_node_sources)
    await seed_exchanges(session, grid_node_sources=grid_node_sources)


@click.command
@click.option("--delete-existing/--keep-existing", default=True)
@click.option(
    "--grid-node-source",
    "grid_node_sources",
    multiple=True,
    type=click.Choice(AVAILABLE_DATA_SOURCES),
)
@make_sync
async def main(delete_existing: bool, grid_node_sources: list[str]) -> None:
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
        if delete_existing:
            for table in Base.metadata.sorted_tables:
                await session.execute(table.delete())
        await session.commit()

        await seed_data(session, grid_node_sources=grid_node_sources)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    main()
