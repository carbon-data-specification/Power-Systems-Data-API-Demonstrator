# SPDX-License-Identifier: Apache-2.0

from typing import List

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from power_systems_data_api_demonstrator.src.lib.db.dependencies import get_db_session
from power_systems_data_api_demonstrator.src.lib.db.models.fuel_types import (
    FuelTypeModel,
)


class FuelTypeNotFoundError(ValueError):
    def __init__(self, fuel_type_name: str):
        super().__init__(f"Could not find a fuel type with name: {fuel_type_name}")


class FuelTypeDAO:
    """Class for accessing fuel_type table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_fuel_type(
        self, fuel_type_model: FuelTypeModel, overwrite_if_exists=True
    ) -> None:
        """
        Add single fuel_type to session.
        :param name: name of a grid_node.
        """
        if overwrite_if_exists:
            delete_stmt = delete(FuelTypeModel).filter_by(name=fuel_type_model.name)
            await self.session.execute(delete_stmt)
        self.session.add(fuel_type_model)
        await self.session.commit()

    async def get_all_fuel_types(self, limit: int | None = None) -> List[FuelTypeModel]:
        """
        Get all fuel types with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(FuelTypeModel).limit(limit),
        )

        return list(raw_dummies.scalars().fetchall())

    async def get_by_name(self, name: str) -> FuelTypeModel:
        """
        Get specific fuel_type model.
        :param name: name of fuel_type instance.
        :return: fuel_type models.
        """
        query = select(FuelTypeModel).where(FuelTypeModel.name == name)
        rows = await self.session.execute(query)
        value = rows.scalars().one_or_none()
        if not value:
            raise FuelTypeNotFoundError(id)
        return value

    async def delete_fuel_type(self, name: str) -> None:
        delete_stmt = delete(FuelTypeModel).filter_by(name=name)
        self.session.execute(delete_stmt)
        await self.session.commit()
