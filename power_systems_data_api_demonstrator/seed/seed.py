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
from power_systems_data_api_demonstrator.src.api.power_system_resource.schema import (
    FuelTypes,
)
from power_systems_data_api_demonstrator.src.lib.config import GRID_NODES
from power_systems_data_api_demonstrator.src.lib.db.base import Base
from power_systems_data_api_demonstrator.src.lib.db.dao.fuel_type_dao import FuelTypeDAO
from power_systems_data_api_demonstrator.src.lib.db.dao.power_system_resource_dao import (
    PsrDAO,
)
from power_systems_data_api_demonstrator.src.lib.db.models.exchanges import (
    ExchangeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.fuel_types import (
    FuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.generation import (
    CapacityForFuelTypeModel,
    GenerationForFuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.power_system_resource_model import (
    PsrModel,
)

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
AVAILABLE_DATA_SOURCES = os.listdir(DATA_DIR)


def get_power_system_resource_by_id(power_system_resource_id: str) -> dict[str, Any]:
    return next(
        power_system_resource
        for power_system_resource in GRID_NODES
        if power_system_resource.get("id") == power_system_resource_id
    )


async def seed_fuel_types(session: AsyncSession) -> None:
    fuel_type_service = FuelTypeDAO(session)
    for fuel_type in FuelTypes:
        await fuel_type_service.create_fuel_type(FuelTypeModel(name=fuel_type))


async def seed_power_system_resources(
    session: AsyncSession, /, *, power_system_resource_sources: list[str]
) -> None:
    power_system_resource_service = PsrDAO(session)
    await power_system_resource_service.delete_all_power_system_resources()
    for grid_source in power_system_resource_sources:
        # From exchanges
        try:
            df_exchanges = pd.read_csv(
                os.path.join(DATA_DIR, grid_source, "imports_exports.csv")
            )
            power_system_resource_ids_from_exchange = set(
                df_exchanges["Grid Node To"].unique()
            ).union(set(df_exchanges["Grid Node From"].unique()))
            for power_system_resource_id in power_system_resource_ids_from_exchange:
                id_ = power_system_resource_id.upper()
                assert id_ in [
                    power_system_resource.get("id")
                    for power_system_resource in GRID_NODES
                ], f"{id_} not in {GRID_NODES}"
                g_n = get_power_system_resource_by_id(id_)
                exists_already = await power_system_resource_service.check_if_power_system_resource_exists(
                    g_n["id"]
                )
                if not exists_already:
                    await power_system_resource_service.create_power_system_resource(
                        PsrModel(
                            id=g_n.get("id"), name=g_n.get("name"), type=g_n.get("type")
                        )
                    )
        except FileNotFoundError:
            logger.error(f"Could not find imports_exports.csv for {grid_source}")
            continue

        # From unit generation
        try:
            # Files
            files = sorted(os.listdir(os.path.join(DATA_DIR, grid_source)))
            for file in files:
                if file.startswith("generation_") and file.endswith(".csv"):
                    df_generation = pd.read_csv(
                        os.path.join(DATA_DIR, grid_source, file)
                    )
                    power_system_resource_ids_from_generation = df_generation[
                        "Grid Node"
                    ].unique()
                    for (
                        power_system_resource_id
                    ) in power_system_resource_ids_from_generation:
                        id_ = power_system_resource_id.upper()
                        assert id_ in [
                            power_system_resource.get("id")
                            for power_system_resource in GRID_NODES
                        ], f"{id_} not in {GRID_NODES}"
                        g_n = get_power_system_resource_by_id(id_)
                        await power_system_resource_service.create_power_system_resource(
                            PsrModel(
                                id=g_n.get("id"),
                                name=g_n.get("name"),
                                type=g_n.get("type"),
                                parent_id=g_n.get("parent_id"),
                            )
                        )

        except FileNotFoundError:
            logger.error(f"Could not find generation.csv for {grid_source}")
            continue


async def seed_generation(
    session: AsyncSession, /, *, power_system_resource_sources: list[str]
) -> None:
    power_system_resource_service = PsrDAO(session)
    for grid_source in power_system_resource_sources:
        try:
            # Overall generation
            df_generation = pd.read_csv(
                os.path.join(DATA_DIR, grid_source, "generation.csv")
            )
            for power_system_resource_id in df_generation["Grid Node"].unique():
                df_this_nodes_generation = df_generation[
                    df_generation["Grid Node"] == power_system_resource_id
                ]
                df_generation_rows = pd.melt(
                    df_this_nodes_generation,
                    id_vars=["Grid Node", "start_datetime", "end_datetime", "unit"],
                    var_name="fuel_type",
                    value_name="value",
                ).reset_index()

                await power_system_resource_service.add_generation_for_fuel_type(
                    [
                        GenerationForFuelTypeModel(
                            start_datetime=pd.to_datetime(row["start_datetime"]),
                            end_datetime=pd.to_datetime(row["end_datetime"]),
                            value=row["value"],
                            fuel_type=row["fuel_type"],
                            unit=row["unit"],
                            power_system_resource_id=power_system_resource_id,
                        )
                        for i, row in df_generation_rows.iterrows()
                    ]
                )
            # Generation per unit
            # Find pattern generation-*.csv
            for file in os.listdir(os.path.join(DATA_DIR, grid_source)):
                if file.startswith("generation_") and file.endswith(".csv"):
                    df_generation = pd.read_csv(
                        os.path.join(DATA_DIR, grid_source, file)
                    )
                    await power_system_resource_service.add_generation_for_fuel_type(
                        [
                            GenerationForFuelTypeModel(
                                start_datetime=pd.to_datetime(row["start_datetime"]),
                                end_datetime=pd.to_datetime(row["end_datetime"]),
                                value=row["value"],
                                fuel_type=row["Fuel Type"],
                                unit=row["unit"],
                                power_system_resource_id=row["Grid Node"],
                            )
                            for i, row in df_generation.iterrows()
                        ]
                    )

        except FileNotFoundError:
            logger.error(f"Could not find generation.csv for {grid_source}")
            continue


async def seed_exchanges(
    session: AsyncSession, /, *, power_system_resource_sources: list[str]
) -> None:
    power_system_resource_service = PsrDAO(session)
    for grid_source in power_system_resource_sources:
        try:
            df_exchanges = pd.read_csv(
                os.path.join(DATA_DIR, grid_source, "imports_exports.csv")
            )

            await power_system_resource_service.add_exchanges(
                [
                    ExchangeModel(
                        start_datetime=pd.to_datetime(row["start_datetime"]),
                        end_datetime=pd.to_datetime(row["end_datetime"]),
                        value=row["Value"],
                        unit=row["unit"],
                        power_system_resource_from_id=row["Grid Node From"],
                        power_system_resource_to_id=row["Grid Node To"],
                    )
                    for i, row in df_exchanges.iterrows()
                ]
            )

        except FileNotFoundError:
            logger.error(f"Could not find imports_exports.csv for {grid_source}")
            continue


async def seed_capacity(
    session: AsyncSession, /, *, power_system_resource_sources: list[str]
) -> None:
    power_system_resource_service = PsrDAO(session)
    for grid_source in power_system_resource_sources:
        try:
            df_capacity = pd.read_csv(
                os.path.join(DATA_DIR, grid_source, "installed_capacity.csv")
            )

            await power_system_resource_service.add_capacities_for_fuel_type(
                [
                    CapacityForFuelTypeModel(
                        power_system_resource_id=row["Grid Node"],
                        start_datetime=pd.to_datetime(row["start_datetime"]),
                        end_datetime=pd.to_datetime(row["end_datetime"]),
                        value=row["Value"],
                        unit=row["unit"],
                        fuel_type=row["Fuel Type"],
                    )
                    for i, row in df_capacity.iterrows()
                ]
            )

        except FileNotFoundError:
            logger.error(f"Could not find imports_exports.csv for {grid_source}")
            continue


def make_sync(func: Callable[P, Awaitable[T]]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        return asyncio.run(func(*args, **kwargs))  # type: ignore

    return wrapper


async def seed_data(
    session: AsyncSession, power_system_resource_sources: list[str] | None = None
) -> None:
    power_system_resource_sources = power_system_resource_sources or sorted(
        set(
            [
                power_system_resource.get("source")
                for power_system_resource in GRID_NODES
                if power_system_resource.get("source")
            ]
        )
    )
    await seed_fuel_types(session)
    await seed_power_system_resources(
        session, power_system_resource_sources=power_system_resource_sources
    )
    await seed_generation(
        session, power_system_resource_sources=power_system_resource_sources
    )
    await seed_exchanges(
        session, power_system_resource_sources=power_system_resource_sources
    )
    await seed_capacity(
        session, power_system_resource_sources=power_system_resource_sources
    )


@click.command
@click.option("--debug-mode/--normal-mode", default=False)
@click.option("--delete-existing/--keep-existing", default=True)
@click.option(
    "--grid-node-source",
    "power_system_resource_sources",
    multiple=True,
    type=click.Choice(AVAILABLE_DATA_SOURCES),
)
@make_sync
async def main(
    delete_existing: bool, power_system_resource_sources: list[str], debug_mode: bool
) -> None:
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
        try:
            if delete_existing:
                for table in Base.metadata.sorted_tables:
                    await session.execute(table.delete())
            await session.commit()

            await seed_data(
                session, power_system_resource_sources=power_system_resource_sources
            )
        except KeyboardInterrupt:
            raise
        except Exception:
            if debug_mode:
                import pdb

                pdb.post_mortem()
            raise

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    main()
