from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from power_systems_data_api_demonstrator.db.dependencies import get_db_session
from power_systems_data_api_demonstrator.db.models.grid_node_model import (
    GridNodeModel,
    GenerationModel,
)


class GridNodeDAO:
    """Class for accessing grid_node table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_grid_node(self, grid_node_model: GridNodeModel) -> None:
        """
        Add single grid_node to session.

        :param name: name of a grid_node.
        """
        self.session.add(grid_node_model)

    async def add_generation(
        self, generation: list[GenerationModel], /, *, grid_node_id: int
    ) -> None:
        """
        Add single grid_node to session.

        :param name: name of a grid_node.
        """
        for gen in generation:
            self.session.add(gen)
        self.session.commit()

    async def get_all_grid_nodes(self, limit: int) -> List[GridNodeModel]:
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

    async def get_by_id(self, id: int) -> List[GridNodeModel]:
        """
        Get specific grid_node model.

        :param name: name of grid_node instance.
        :return: grid_node models.
        """
        query = select(GridNodeModel).where(GridNodeModel.id == id)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
