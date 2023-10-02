# SPDX-License-Identifier: Apache-2.0

import json
from datetime import datetime
from typing import List

from fastapi import Depends
from pydantic import BaseModel, validator
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from power_systems_data_api_demonstrator.src.lib.db.dependencies import get_db_session
from power_systems_data_api_demonstrator.src.lib.db.models.demand import DemandModel
from power_systems_data_api_demonstrator.src.lib.db.models.exchanges import (
    ExchangeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.generation import (
    CapacityForFuelTypeModel,
    FuelTypes,
    GenerationForFuelTypeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.power_system_resource_model import (
    PsrModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.prices import (
    DayAheadPriceModel,
)


class PsrNotFoundError(ValueError):
    def __init__(self, power_system_resource_id: str):
        super().__init__(
            f"Could not find a grid node with id: {power_system_resource_id}"
        )


class GenerationDTO(BaseModel):
    power_system_resource_id: str
    start_datetime: datetime
    end_datetime: datetime
    value: float
    unit: str
    generation_by_fuel_type: dict[FuelTypes, float]

    @validator("generation_by_fuel_type", pre=True)
    def convert_to_json(
        cls: "GenerationDTO", value: str | dict[FuelTypes, float]
    ) -> dict[FuelTypes, float]:
        if isinstance(value, str):
            return json.loads(value)
        else:
            return value

    class Config:
        orm_mode = True


class PsrDAO:
    """Class for accessing power_system_resource table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def delete_all_power_system_resources(self) -> None:
        delete_stmt = delete(PsrModel)
        await self.session.execute(delete_stmt)
        await self.session.commit()

    async def create_power_system_resource(
        self, power_system_resource_model: PsrModel
    ) -> None:
        """
        Add single power_system_resource to session.
        :param name: name of a power_system_resource.
        """
        self.session.add(power_system_resource_model)
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
        self, power_system_resource_id: str
    ) -> list[GenerationDTO]:
        """
        Add single generation_per_fuel_type.
        """
        """
        generation_for_fuel_types_sql = await self.session.execute(
            select(GenerationForFuelTypeModel).filter(
                GenerationForFuelTypeModel.power_system_resource_id == power_system_resource_id
            ),
        )
        """
        raw_generation = await self.session.execute(
            select(
                GenerationForFuelTypeModel.power_system_resource_id,
                GenerationForFuelTypeModel.start_datetime,
                GenerationForFuelTypeModel.end_datetime,
                func.sum(GenerationForFuelTypeModel.value).label("value"),
                func.min(GenerationForFuelTypeModel.unit).label("unit"),
                func.json_group_object(
                    GenerationForFuelTypeModel.fuel_type,
                    GenerationForFuelTypeModel.value,
                ).label("generation_by_fuel_type"),
            )
            .filter(
                GenerationForFuelTypeModel.power_system_resource_id
                == power_system_resource_id
            )
            .group_by(
                GenerationForFuelTypeModel.power_system_resource_id,
                GenerationForFuelTypeModel.start_datetime,
                GenerationForFuelTypeModel.end_datetime,
            )
        )
        return [GenerationDTO.from_orm(row) for row in raw_generation.all()]

    async def get_day_ahead_price(
        self, power_system_resource_id: str
    ) -> list[DayAheadPriceModel]:
        """
        Add single generation_per_fuel_type.
        """
        raw_generation = await self.session.execute(
            select(DayAheadPriceModel).filter(
                DayAheadPriceModel.power_system_resource_id == power_system_resource_id
            ),
        )
        generation_for_fuel_types = list(raw_generation.scalars().fetchall())
        return generation_for_fuel_types

    async def get_imports(self, power_system_resource_id: str) -> list[ExchangeModel]:
        """
        Get imports to a grid node.
        """
        raw_imports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.power_system_resource_to_id == power_system_resource_id,
                ExchangeModel.value > 0,
            ),
        )
        imports = list(raw_imports.scalars().fetchall())
        raw_exports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.power_system_resource_from_id == power_system_resource_id,
                ExchangeModel.value < 0,
            ),
        )
        exports = list(raw_exports.scalars().fetchall())
        exports = [
            ExchangeModel(
                power_system_resource_from_id=exp.power_system_resource_to_id,
                power_system_resource_to_id=exp.power_system_resource_from_id,
                value=-1 * exp.value,
                start_datetime=exp.start_datetime,
                end_datetime=exp.end_datetime,
                unit=exp.unit,
            )
            for exp in exports
        ]
        return imports + exports

    async def get_exports(self, power_system_resource_id: str) -> list[ExchangeModel]:
        """
        Get exports from a grid node.
        """
        raw_imports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.power_system_resource_to_id == power_system_resource_id,
                ExchangeModel.value < 0,
            ),
        )
        imports = list(raw_imports.scalars().fetchall())
        imports = [
            ExchangeModel(
                power_system_resource_from_id=imp.power_system_resource_to_id,
                power_system_resource_to_id=imp.power_system_resource_from_id,
                value=-1 * imp.value,
                start_datetime=imp.start_datetime,
                end_datetime=imp.end_datetime,
                unit=imp.unit,
            )
            for imp in imports
        ]
        raw_exports = await self.session.execute(
            select(ExchangeModel).filter(
                ExchangeModel.power_system_resource_from_id == power_system_resource_id,
                ExchangeModel.value > 0,
            ),
        )
        exports = list(raw_exports.scalars().fetchall())
        return imports + exports

    async def get_capacity(
        self, power_system_resource_id: str
    ) -> list[CapacityForFuelTypeModel]:
        """
        Get capacity of a grid node.
        """
        raw_capacity = await self.session.execute(
            select(CapacityForFuelTypeModel).filter(
                CapacityForFuelTypeModel.power_system_resource_id
                == power_system_resource_id
            ),
        )
        capacity = list(raw_capacity.scalars().fetchall())
        return capacity

    async def get_demand(self, power_system_resource_id: str) -> list[DemandModel]:
        """
        Get demand of a grid node.
        """
        raw_demand = await self.session.execute(
            select(DemandModel).filter(
                DemandModel.power_system_resource_id == power_system_resource_id
            ),
        )
        demand = list(raw_demand.scalars().fetchall())
        return demand

    async def get_all_power_system_resources(
        self, limit: int | None = None
    ) -> List[PsrModel]:
        """
        Get all power_system_resource models with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_power_system_resources = await self.session.execute(
            select(PsrModel).limit(limit),
        )

        return list(raw_power_system_resources.scalars().fetchall())

    async def get_power_system_resource_with_parent_id(self, id: str) -> List[PsrModel]:
        """
        Get all power_system_resource models with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_power_system_resources = await self.session.execute(
            select(PsrModel).filter(PsrModel.parent_id == id),
        )

        return list(raw_power_system_resources.scalars().fetchall())

    async def get_by_id(self, id: str) -> PsrModel:
        """
        Get specific power_system_resource model.
        :param name: name of power_system_resource instance.
        :return: power_system_resource models.
        """
        query = select(PsrModel).where(PsrModel.id == id)
        rows = await self.session.execute(query)
        value = rows.scalars().one_or_none()
        if not value:
            raise PsrNotFoundError(id)
        return value

    async def check_if_power_system_resource_exists(self, id: str) -> bool:
        """
        Get specific power_system_resource model.
        :param name: name of power_system_resource instance.
        :return: power_system_resource models.
        """
        query = select(PsrModel).where(PsrModel.id == id)
        rows = await self.session.execute(query)
        return rows.scalars().one_or_none() is not None

    async def delete_power_system_resource(self, id: str) -> None:
        delete_stmt = delete(PsrModel).filter_by(id=id)
        await self.session.execute(delete_stmt)
        await self.session.commit()
