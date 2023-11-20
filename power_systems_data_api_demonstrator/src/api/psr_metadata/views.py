from typing import Annotated, Optional

from fastapi import APIRouter, Path
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
    "/power-system-resources",
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
