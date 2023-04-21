# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from enum import Enum
from typing import Dict, List

from pydantic import BaseModel

from power_systems_data_api_demonstrator.src.lib.db.models.generation import FuelTypes


class GridTopologyLevel(str, Enum):
    GENERATION_UNIT = "GENERATION_UNIT"
    POWER_PLANT = "POWER_PLANT"
    SUBSTATION = "SUBSTATION"
    MARKET = "MARKET"
    SYSTEM = "SYSTEM"


class GridNodeDTO(BaseModel):
    """
    DTO for grid node models.
    It returned when accessing dummy models from the API.
    """

    id: str
    parent_id: str | None
    children_ids: List[str] | None
    name: str
    type: GridTopologyLevel

    class Config:
        orm_mode = True


class ExchangeDTO(BaseModel):
    """
    DTO for exchange models.
    It returned when accessing dummy models from the API.
    """

    grid_node_from_id: str
    grid_node_to_id: str
    start_datetime: datetime
    end_datetime: datetime
    value: float
    unit: str

    class Config:
        orm_mode = True


class DemandDTO(BaseModel):
    """
    DTO for demand models.
    It returned when accessing dummy models from the API.
    """

    grid_node_id: str
    start_datetime: datetime
    end_datetime: datetime
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
    start_datetime: datetime
    end_datetime: datetime
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
    start_datetime: datetime
    end_datetime: datetime
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
    start_datetime: datetime
    end_datetime: datetime
    generation_capacity: Dict[FuelTypes, float]
    unit: str

    @property
    def total_generation_capacity(self) -> float:
        return sum(self.generation_capacity.values())
