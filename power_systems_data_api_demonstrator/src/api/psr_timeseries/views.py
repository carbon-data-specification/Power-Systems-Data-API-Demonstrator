from pydantic import BaseModel
from sqlmodel import select

from sqlmodel import Session
from enum import Enum
from sqlmodel import Field
from datetime import datetime
from sqlmodel import SQLModel

from fastapi import APIRouter, Request
from fastapi.param_functions import Depends
from power_systems_data_api_demonstrator.src.api.db import get_session


router = APIRouter()


class PsrGenerationRequest(BaseModel):
    id: str
    start_datetime: datetime
    end_datetime: datetime


class ElectricityUnit(str, Enum):
    mwh = "MWh"
    kwh = "kWh"
    wh = "Wh"


class FuelSourceValue(BaseModel):
    technology: str
    type: str
    value: float


class PsrGeneration(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    value: float
    value_by_fuel_source: list[FuelSourceValue]


class PsrGenerationResponse(BaseModel):
    id: str
    unit: ElectricityUnit
    generation: PsrGeneration


class GenerationByFuelSourceTable(SQLModel):
    start_datetime: datetime = Field(primary_key=True)
    end_datetime: datetime = Field(primary_key=True)
    type: str = Field(primary_key=True, foreign_key="fuel_type.name")
    technology: str = Field(primary_key=True, foreign_key="fuel_technology.name")
    value: float


class FuelType(SQLModel):
    name: str
    external_id: str


class FuelTechnology(SQLModel):
    name: str
    external_id: str


@router.get(
    "/{id}/timeseries/generation",
    summary="generation",
)
async def get_generation(
    session: Session = Depends(get_session),
) -> PsrGenerationResponse:
    return {}
