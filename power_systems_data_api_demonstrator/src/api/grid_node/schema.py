# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from power_systems_data_api_demonstrator.src.lib.db.models.generation import FuelTypes


class GridNodeType(str, Enum):
    GENERATION_UNIT = "GENERATION_UNIT"
    PRODUCTION_UNIT = "PRODUCTION_UNIT"
    SUBSTATION = "SUBSTATION"
    MARKET = "MARKET"
    SYSTEM = "SYSTEM"


class GridNodeModelDTO(BaseModel):
    """
    DTO for grid node models.
    It returned when accessing dummy models from the API.
    """

    id: str
    name: str
    type: GridNodeType

    class Config:
        orm_mode = True


class GenerationDTO(BaseModel):
    """
    DTO for generation models.
    It returned when accessing dummy models from the API.
    """

    grid_node_id: str
    datetime: datetime
    value: float
    unit: str
    fuel_type: FuelTypes

    class Config:
        orm_mode = True
