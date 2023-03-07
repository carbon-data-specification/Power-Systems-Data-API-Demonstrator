from pydantic import BaseModel
from enum import auto
from enum import Enum


class GridNodeType(str, Enum):
    GENERATION_UNIT = "GENERATION_UNIT"
    PRODUCTION_UNIT = "PRODUCTION_UNIT"
    SUBSTATION = "SUBSTATION"
    MARKET = "MARKET"
    SYSTEM = "SYSTEM"


class FuelTypes(str, Enum):
    BROWN_COAL = "BROWN_COAL"
    HARD_COAL = "HARD_COAL"
    COAL_DERIVED_GAS = "COAL_DERIVED_GAS"
    OTHER_COAL = "OTHER_COAL"
    NATURAL_GAS = "NATURAL_GAS"
    LANDFILL_GAS = "LANDFILL_GAS"
    OTHER_GAS = "OTHER_GAS"
    WOOD = "WOOD"
    MUNICIPAL_WASTE = "MUNICIPAL_WASTE"
    PROPANE_OIL = "PROPANE_OIL"
    SHALE_OIL = "SHALE_OIL"
    DISTILLATE_OIL = "DISTILLATE_OIL"
    OTHER_OIL = "OTHER_OIL"
    PEAT = "PEAT"
    URANIUM = "URANIUM"
    THORIUM = "THORIUM"
    PLUTONIUM = "PLUTONIUM"
    SOLAR = "SOLAR"
    WIND = "WIND"
    GEOTHERMAL = "GEOTHERMAL"
    WATER = "WATER"


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
