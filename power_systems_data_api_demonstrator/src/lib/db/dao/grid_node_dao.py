# SPDX-License-Identifier: Apache-2.0

from typing import List

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from power_systems_data_api_demonstrator.src.lib.db.dependencies import get_db_session
from power_systems_data_api_demonstrator.src.lib.db.models.demand import DemandModel
from power_systems_data_api_demonstrator.src.lib.db.models.exchanges import (
    ExchangeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.generation import (
    CapacityForFuelTypeModel,
    GenerationForFuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GridNodeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.prices import (
    DayAheadPriceModel,
)


class GridNodeNotFoundError(ValueError):
    def __init__(self, grid_node_id: str):
        super().__init__(f"Could not find a grid node with id: {grid_node_id}")


class GridNodeDAO:
    """Class for accessing grid_node table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_grid_node(
        self, grid_node_model: GridNodeModel, overwrite_if_exists: bool = True
    ) -> None:
        """
        Add single grid_node to session.
        :param name: name of a grid_node.
        """
        if overwrite_if_exists:
            delete_stmt = delete(GridNodeModel).filter_by(id=grid_node_model.id)
            await self.session.execute(delete_stmt)
        self.session.add(grid_node_model)
        await self.session.commit()

    async def add_generation_for_fuel_type(
        self,
        generation_for_fuel_type: list[GenerationForFuelTypeModel],
    ) -> None:
        """
        Add single generation_per_fuel_type.
        """
        for gen in generation_for_fuel_type:
            self.session.add(gen)
        await self.session.commit()

    async def add_exchanges(self, exchanges: list[ExchangeModel]) -> None:
        """
        Add single generation_per_fuel_type.
        """
        for exchange in exchanges:
            self.session.add(exchange)
        await self.session.commit()

    async def add_demand(self, demand: list[DemandModel]) -> None:
        """
        Add single demand.
        """
        for demand_entry in demand:
            self.session.add(demand_entry)
        await self.session.commit()

    async def add_capacities_for_fuel_type(
        self,
        capacities_for_fuel_type: list[CapacityForFuelTypeModel],
    ) -> None:
        """
        Add single generation_per_fuel_type.
        """
        for capacity in capacities_for_fuel_type:
            self.session.add(capacity)
        await self.session.commit()

    async def get_generation(
        self, grid_node_id: str
    ) -> list[GenerationForFuelTypeModel]:
        """
        Add single generation_per_fuel_type.
        """
        raw_generation = await self.session.execute(
            select(GenerationForFuelTypeModel).filter(
                GenerationForFuelTypeModel.grid_node_id == grid_node_id
            ),
        )
        generation_for_fuel_types = list(raw_generation.scalars().fetchall())
        return generation_for_fuel_types

    async def get_day_ahead_price(self, grid_node_id: str) -> list[DayAheadPriceModel]:
        """
        Add single generation_per_fuel_type.
        """
        raw_generation = await self.session.execute(
            select(DayAheadPriceModel).filter(
                DayAheadPriceModel.grid_node_id == grid_node_id
            ),
        )
        generation_for_fuel_types = list(raw_generation.scalars().fetchall())
        return generation_for_fuel_types

    async def get_imports(self, grid_node_id: str) -> list[ExchangeModel]:
        """
        Get imports to a grid node.
        """
        raw_imports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.grid_node_to_id == grid_node_id, ExchangeModel.value > 0
            ),
        )
        imports = list(raw_imports.scalars().fetchall())
        raw_exports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.grid_node_from_id == grid_node_id, ExchangeModel.value < 0
            ),
        )
        exports = list(raw_exports.scalars().fetchall())
        exports = [
            ExchangeModel(
                grid_node_from_id=exp.grid_node_to_id,
                grid_node_to_id=exp.grid_node_from_id,
                value=-1 * exp.value,
                datetime=exp.datetime,
                unit=exp.unit,
            )
            for exp in exports
        ]
        return imports + exports

    async def get_exports(self, grid_node_id: str) -> list[ExchangeModel]:
        """
        Get exports from a grid node.
        """
        raw_imports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.grid_node_to_id == grid_node_id, ExchangeModel.value < 0
            ),
        )
        imports = list(raw_imports.scalars().fetchall())
        imports = [
            ExchangeModel(
                grid_node_from_id=imp.grid_node_to_id,
                grid_node_to_id=imp.grid_node_from_id,
                value=-1 * imp.value,
                datetime=imp.datetime,
                unit=imp.unit,
            )
            for imp in imports
        ]
        raw_exports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.grid_node_from_id == grid_node_id, ExchangeModel.value > 0
            ),
        )
        exports = list(raw_exports.scalars().fetchall())
        return imports + exports

    async def get_capacity(self, grid_node_id: str) -> list[CapacityForFuelTypeModel]:
        """
        Get capacity of a grid node.
        """
        raw_capacity = await self.session.execute(
            select(CapacityForFuelTypeModel).filter(
                CapacityForFuelTypeModel.grid_node_id == grid_node_id
            ),
        )
        capacity = list(raw_capacity.scalars().fetchall())
        return capacity

    async def get_demand(self, grid_node_id: str) -> list[DemandModel]:
        """
        Get demand of a grid node.
        """
        raw_demand = await self.session.execute(
            select(DemandModel).filter(DemandModel.grid_node_id == grid_node_id),
        )
        demand = list(raw_demand.scalars().fetchall())
        return demand

    async def get_all_grid_nodes(self, limit: int | None = None) -> List[GridNodeModel]:
        """
        Get all grid_node models with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_grid_nodes = await self.session.execute(
            select(GridNodeModel).limit(limit),
        )

        return list(raw_grid_nodes.scalars().fetchall())

    async def get_by_id(self, id: str) -> GridNodeModel:
        """
        Get specific grid_node model.
        :param name: name of grid_node instance.
        :return: grid_node models.
        """
        query = select(GridNodeModel).where(GridNodeModel.id == id)
        rows = await self.session.execute(query)
        value = rows.scalars().one_or_none()
        if not value:
            raise GridNodeNotFoundError(id)
        return value

    async def delete_grid_node(self, id: str) -> None:
        delete_stmt = delete(GridNodeModel).filter_by(id=id)
        await self.session.execute(delete_stmt)
        await self.session.commit()
