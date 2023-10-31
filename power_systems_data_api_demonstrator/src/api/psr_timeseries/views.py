from pydantic import BaseModel
from zoneinfo import ZoneInfo
from fastapi import Path
from fastapi import Query
from typing import Annotated
import pandas as pd
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


class ElectricityUnit(str, Enum):
    mwh = "MWh"
    kwh = "kWh"
    wh = "Wh"


class FuelType(SQLModel, table=True):
    name: str = Field(primary_key=True)
    external_id: str | None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: "FuelType") -> bool:
        return self.name == other.name


class FuelTechnology(SQLModel, table=True):
    name: str = Field(primary_key=True)
    external_id: str | None

    def __hash__(self):
        return hash(self.name)


class GenerationByFuelSource(SQLModel):
    id: str = Field(primary_key=True)
    type: str = Field(primary_key=True, foreign_key="fueltype.name")
    technology: str | None = Field(
        primary_key=True, foreign_key="fueltechnology.name", nullable=True
    )
    value: float


class GenerationByFuelSourceTable(GenerationByFuelSource, table=True):
    start_datetime: datetime = Field(primary_key=True)
    end_datetime: datetime = Field(primary_key=True)
    timezone: str = Field(default="UTC")
    unit: ElectricityUnit


class Generation(SQLModel):
    start_datetime: datetime
    end_datetime: datetime
    value: float
    value_by_fuel_source: list[GenerationByFuelSource]


class GenerationResponse(SQLModel):
    id: str
    unit: ElectricityUnit | None
    generation: list[Generation]

    @classmethod
    def empty(cls, id: str):
        return cls(id=id, unit=None, generation=[])


class GenerationRequest(SQLModel):
    id: str
    start_datetime: datetime
    end_datetime: datetime


@router.get(
    "/{id}/timeseries/generation",
    summary="generation",
)
async def get_generation(
    id: Annotated[str, Path(description="PSR id (try US-WECC-CISO)")],
    start_datetime: Annotated[
        datetime, Query(alias="startDatetime", description="Start datetime")
    ] = datetime(2021, 6, 1, tzinfo=ZoneInfo("UTC")),
    end_datetime: Annotated[
        datetime, Query(alias="endDatetime", description="End datetime")
    ] = datetime(2021, 6, 2, tzinfo=ZoneInfo("UTC")),
    session: Session = Depends(get_session),
) -> GenerationResponse:
    result = session.execute(
        select(GenerationByFuelSourceTable)
        .filter_by(id=id)
        .filter(
            GenerationByFuelSourceTable.start_datetime >= start_datetime,
            GenerationByFuelSourceTable.end_datetime <= end_datetime,
        )
    )
    generation = result.scalars().all()
    if not generation:
        return GenerationResponse.empty(id=id)
    units = list(set([g.unit for g in generation]))
    if len(units) > 1:
        raise ValueError(
            "There are multiple units of generation in this data and this has not yet been implemented"
        )
    unit = units[0]
    df = pd.DataFrame([g.dict() for g in generation])

    generation = []
    unique_dts = df[["start_datetime", "end_datetime", "timezone"]].drop_duplicates()
    for _, dt in unique_dts.iterrows():
        rows = df[
            (df["start_datetime"] == dt["start_datetime"])
            & (df["end_datetime"] == dt["end_datetime"])
        ]
        generation.append(
            Generation(
                start_datetime=dt["start_datetime"].tz_localize(dt["timezone"]),
                end_datetime=dt["end_datetime"].tz_localize(dt["timezone"]),
                value=rows["value"].sum(),
                value_by_fuel_source=[
                    GenerationByFuelSource(
                        id=row["id"],
                        technology=row["technology"],
                        value=row["value"],
                        type=row["type"],
                    )
                    for _, row in rows.iterrows()
                ],
            )
        )

    return GenerationResponse(id=id, unit=unit, generation=generation)
