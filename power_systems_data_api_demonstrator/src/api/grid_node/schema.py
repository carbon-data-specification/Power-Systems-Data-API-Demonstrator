from enum import Enum, auto

from pydantic import BaseModel


class GridNodeType(Enum):
    GENERATION_UNIT = auto()
    PRODUCTION_UNIT = auto()
    SUBSTATION = auto()
    MARKET = auto()
    SYSTEM = auto()


class FuelTypes(str, Enum):
    BROWN_COAL = auto()
    HARD_COAL = auto()
    COAL_DERIVED_GAS = auto()
    OTHER_COAL = auto()
    NATURAL_GAS = auto()
    LANDFILL_GAS = auto()
    OTHER_GAS = auto()
    WOOD = auto()
    MUNICIPAL_WASTE = auto()
    PROPANE_OIL = auto()
    SHALE_OIL = auto()
    DISTILLATE_OIL = auto()
    OTHER_OIL = auto()
    PEAT = auto()
    URANIUM = auto()
    THORIUM = auto()
    PLUTONIUM = auto()
    SOLAR = auto()
    WIND = auto()
    GEOTHERMAL = auto()
    WATER = auto()


class GridNodeModelDTO(BaseModel):
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    id: int
    name: str
    type: GridNodeType

    class Config:
        orm_mode = True
