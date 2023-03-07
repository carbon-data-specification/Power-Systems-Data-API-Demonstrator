from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from power_systems_data_api_demonstrator.db.dao.grid_node_dao import GridNodeDAO
from power_systems_data_api_demonstrator.db.models.grid_node_model import GridNodeModel
from power_systems_data_api_demonstrator.web.api.grid_node.schema import (
    GridNodeModelDTO,
)

router = APIRouter()


@router.get("/list", response_model=List[GridNodeModelDTO])
async def get_grid_nodes(
    limit: int = 10,
    grid_node_dao: GridNodeDAO = Depends(),
) -> List[GridNodeModel]:
    """
    Retrieve all grid nodes from the database.

    :param limit: limit of grid nodes, defaults to 10.
    :param grid_node_dao: DAO for grid nodes.
    :return: list of grid nodes from database.
    """
    return await grid_node_dao.get_all_grid_nodes(limit=limit)


@router.get("/describe/{gride_node_id}", response_model=GridNodeModelDTO)
async def get_grid_nodes(
    id: int,
    grid_node_dao: GridNodeDAO = Depends(),
) -> GridNodeModel:
    """
    Retrieve a description of a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    return await grid_node_dao.get_by_id(grid_node_id)


@router.get("/generation/{gride_node_id}", response_model=GridNodeModelDTO)
async def get_grid_nodes(
    id: int,
    grid_node_dao: GridNodeDAO = Depends(),
) -> GridNodeModel:
    """
    Retrieve a description of a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    return await grid_node_dao.get_by_id(grid_node_id)
