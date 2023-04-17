# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from enum import Enum
from typing import Dict

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


class ExchangeDTO(BaseModel):
    """
    DTO for exchange models.
    It returned when accessing dummy models from the API.
    """

    grid_node_from_id: str
    grid_node_to_id: str
    datetime: datetime
    value: float
    unit: str

    class Config:
        orm_mode = True


class DayAheadPriceDTO(BaseModel):
    """
    DTO for day ahead price models.
    It returned when accessing dummy models from the API.
    """

    grid_node_id: str
    datetime: datetime
    value: float
    currency: str

    class Config:
        orm_mode = True


class CapacityForFuelTypeDTO(BaseModel):
    """
    DTO for capacity models.
    It returned when accessing dummy models from the API.
    """

    grid_node_id: str
    datetime: datetime
    value: float
    fuel_type: FuelTypes
    unit: str

    class Config:
        orm_mode = True


class CapacityDTO(BaseModel):
    """
    DTO for capacity models.
    It returned when accessing dummy models from the API.
    """

    grid_node_id: str
    datetime: datetime
    generation_capacity: Dict[FuelTypes, float]
    unit: str

    @property
    def total_generation_capacity(self) -> float:
        return sum(self.generation_capacity.values())
