from enum import Enum
from typing import Annotated, Optional

import pandas as pd
from fastapi import APIRouter, Path, Query
from fastapi.param_functions import Depends
from sqlmodel import Field, Session, SQLModel, select

from power_systems_data_api_demonstrator.src.api.db import get_session

router = APIRouter()


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


class PowerUnit(str, Enum):
    mw = "MW"
    kw = "kW"
    w = "W"


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
