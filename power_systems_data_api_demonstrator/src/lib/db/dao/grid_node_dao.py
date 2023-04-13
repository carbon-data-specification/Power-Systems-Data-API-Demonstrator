# SPDX-License-Identifier: Apache-2.0

from typing import List

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from power_systems_data_api_demonstrator.src.lib.db.dependencies import get_db_session
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GenerationModel,
    GridNodeModel,
)


class GridNodeNotFoundError(ValueError):
    def __init__(self, grid_node_id: str):
        super().__init__(f"Could not find a grid node with id: {grid_node_id}")


class GridNodeDAO:
    """Class for accessing grid_node table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_grid_node(
        self, grid_node_model: GridNodeModel, overwrite_if_exists=True
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

    async def add_generation(
        self, generation: list[GenerationModel], /, *, grid_node_id: int
    ) -> None:
        """
        Add single grid_node to session.
        :param name: name of a grid_node.
        """
        for gen in generation:
            self.session.add(gen)
        await self.session.commit()

    async def get_all_grid_nodes(self, limit: int | None = None) -> List[GridNodeModel]:
        """
        Get all grid_node models with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(GridNodeModel).limit(limit),
        )

        return list(raw_dummies.scalars().fetchall())

    async def get_by_id(self, id: int) -> GridNodeModel:
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
        self.session.execute(delete_stmt)
        await self.session.commit()
