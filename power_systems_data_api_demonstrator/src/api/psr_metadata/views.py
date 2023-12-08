from enum import Enum
from typing import Annotated, Optional, Sequence

import pandas as pd
from fastapi import APIRouter, Path, Query
from fastapi.param_functions import Depends
from sqlmodel import Field, Session, SQLModel, select

from power_systems_data_api_demonstrator.src.api.db import get_session

router = APIRouter()


class PowerUnit(str, Enum):
    mw = "MW"
    kw = "kW"
    w = "W"


class PSRList(SQLModel, table=True):
    id: str = Field(primary_key=True)
    level: int
    name: Optional[str]


class PSRListResponse(SQLModel):
    psr_list: list[PSRList]


class PSRListReqest(SQLModel):
    level: int


@router.get(
    "/power-system-resource",
    summary="PSR LIST",
)
async def get_psr_list(
    level: Annotated[Optional[int], Path(description="Filter by level")] | None = None,
    session: Session = Depends(get_session),
) -> PSRListResponse:
    if level is None:
        result = session.execute(select(PSRList))
    else:
        result = session.execute(select(PSRList).filter_by(level=level))
    psr_list = result.scalars().all()
    return PSRListResponse(psr_list=psr_list)


class PSR(SQLModel):
    id: str


class PSRInterconnection(SQLModel):
    # connectedPSR: PSR
    connectedPSR: str = Field(primary_key=True)
    value: float


class PSRInterconnectionTable(PSRInterconnection, table=True):
    id: str = Field(primary_key=True)
    unit: PowerUnit


class PSRCapacity(SQLModel):
    id: str = Field(primary_key=True)
    unit: PowerUnit
    transmissionCapacity: list[PSRInterconnection]


class PSRCapacityResponse(SQLModel):
    capacity: list[PSRCapacity]


class Capacity(SQLModel):
    value: float
    startDatetime: str = Field(primary_key=True)
    endDatetime: Optional[str] = None


class CapacityTable(Capacity, table=True):
    id: str = Field(primary_key=True)
    type: str = Field(primary_key=True)
    unit: PowerUnit
    technology: str


class FuelSource(SQLModel):
    technology: str
    type: str
    unit: PowerUnit
    capacity: list[Capacity]


class FuelSourceCapacity(SQLModel):
    id: str = Field(primary_key=True)
    fuelSource: list[FuelSource]


class FuelSourceCapacityResponse(SQLModel):
    capacity: Sequence[FuelSourceCapacity]


@router.get(
    "/power-system-resource/capacity",
    summary="PSR CAPACITY",
)
async def get_psr_capacity(
    id: Annotated[str, Query(description="Filter by PSR")] = "US-WECC-CISO",
    session: Session = Depends(get_session),
) -> FuelSourceCapacityResponse:
    result = session.execute(select(CapacityTable).filter_by(id=id))
    psr_capacity = result.scalars().all()
    df = pd.DataFrame(g.dict() for g in psr_capacity)
    print("This is the basic df")
    print(df)
    print(df.columns)

    # colapse the data frame to a single row per id and unit
    df_psr_capacity = (
        df.groupby(["id", "unit", "technology", "type"])
        .agg(
            {
                "value": lambda x: list(x),
                "startDatetime": lambda x: list(x),
                "endDatetime": lambda x: list(x),
            }
        )
        .copy()
        .reset_index()
    )

    print("This is after grouby")
    print(df_psr_capacity.to_string())
    print(df_psr_capacity.columns)

    # print("this is psr capacity")
    # print(df_psr_capacity)

    psr_capacity = []
    psr_capacity.append(
        FuelSourceCapacity(
            id=df_psr_capacity.loc[0, "id"],
            fuelSource=[
                FuelSource(
                    technology=row["technology"],
                    type=row["type"],
                    unit=row["unit"],
                    capacity=[
                        Capacity(
                            value=row["value"][i],
                            startDatetime=row["startDatetime"][i],
                            endDatetime=row["endDatetime"][i],
                        )
                        for i in range(len(row["startDatetime"]))
                    ],
                )
                for index, row in df_psr_capacity.iterrows()
            ],
        )
    )

    return FuelSourceCapacityResponse(capacity=psr_capacity)


@router.get(
    "/power-system-resource/transmission-capacity",
    summary="TRANSMISSION CAPACITY",
)
async def get_psr_transmission_capacity(
    id: Annotated[str, Query(description="Filter by PSR")] = "US-WECC-CISO",
    session: Session = Depends(get_session),
) -> PSRCapacityResponse:
    result = session.execute(select(PSRInterconnectionTable).filter_by(id=id))
    psr_capacity = result.scalars().all()
    df = pd.DataFrame(g.dict() for g in psr_capacity)
    # colapse the data frame to a single row per id and unit
    df_psr_interconnections = (
        df.groupby(["id", "unit"])
        .agg({"connectedPSR": lambda x: list(x), "value": lambda x: list(x)})
        .reset_index()
    )

    number_of_interconnections = df_psr_interconnections["connectedPSR"].apply(len)[0]

    psr_capacity = []
    psr_capacity.append(
        PSRCapacity(
            id=df_psr_interconnections.loc[0, "id"],
            unit=df_psr_interconnections.loc[0, "unit"],
            transmissionCapacity=[
                PSRInterconnection(
                    connectedPSR=df_psr_interconnections["connectedPSR"].str[i][0],
                    value=df_psr_interconnections["value"].str[i][0],
                )
                for i in range(number_of_interconnections)
            ],
        )
    )

    return PSRCapacityResponse(capacity=psr_capacity)
