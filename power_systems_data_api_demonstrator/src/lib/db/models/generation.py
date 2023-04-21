# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class EnergyUnit(str, Enum):
    mwh = "MWh"
    kwh = "kWh"


class FuelTypes(str, Enum):
    BIOMASS = "BIOMASS"
    BROWN_COAL = "BROWN_COAL"
    HARD_COAL = "HARD_COAL"
    COAL_DERIVED_GAS = "COAL_DERIVED_GAS"
    OTHER_COAL = "OTHER_COAL"
    NATURAL_GAS = "NATURAL_GAS"
    LANDFILL_GAS = "LANDFILL_GAS"
    OTHER_GAS = "OTHER_GAS"
    WOOD = "WOOD"
    MUNICIPAL_WASTE = "MUNICIPAL_WASTE"
    OIL = "OIL"
    PROPANE_OIL = "PROPANE_OIL"
    SHALE_OIL = "SHALE_OIL"
    DISTILLATE_OIL = "DISTILLATE_OIL"
    OTHER_OIL = "OTHER_OIL"
    OTHER_RENEWABLE = "OTHER_RENEWABLE"
    OTHER = "OTHER"
    PEAT = "PEAT"
    URANIUM = "URANIUM"
    THORIUM = "THORIUM"
    PLUTONIUM = "PLUTONIUM"
    SOLAR = "SOLAR"
    WIND = "WIND"
    WIND_ON_SHORE = "WIND_ON_SHORE"
    WIND_OFF_SHORE = "WIND_OFF_SHORE"
    GEOTHERMAL = "GEOTHERMAL"
    HYDRO = "HYDRO"
    HYDRO_RUN_OF_RIVER = "HYDRO_RUN_OF_RIVER"
    HYDRO_RESERVOIR = "HYDRO_RESERVOIR"
    HYDRO_PUMPED_STORAGE = "HYDRO_PUMPED_STORAGE"
    HYDRO_PUMPED_STORAGE_CONSUMPTION = "HYDRO_PUMPED_STORAGE_CONSUMPTION"
    WATE = "WASTE"
    NUCLEAR = "NUCLEAR"


class GenerationForFuelTypeModel(Base):
    """Model of grid node generation for a given fuel type."""

    __tablename__ = "generation_per_fuel_type"

    grid_node_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float]
    unit: Mapped[str]
    fuel_type: Mapped[str] = mapped_column(
        ForeignKey("fuel_type.name"), primary_key=True
    )


class CapacityForFuelTypeModel(Base):
    """Model of grid node generation for a given fuel type."""

    __tablename__ = "capacity_per_fuel_type"

    grid_node_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float]
    unit: Mapped[str]
    fuel_type: Mapped[str] = mapped_column(
        ForeignKey("fuel_type.name"), primary_key=True
    )
