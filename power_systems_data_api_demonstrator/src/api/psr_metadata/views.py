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


class DescribeResponse(BaseModel):
    pass


@router.get(
    "/{id}/describe",
    summary="TOPOLOGY DESCRIPTION",
)
async def get_topology_levels(
    id: int,
    session: Session = Depends(get_session),
) -> DescribeResponse:
    return {}
