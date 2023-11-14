from typing import Sequence

from fastapi import APIRouter
from fastapi.param_functions import Depends
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, select

from power_systems_data_api_demonstrator.src.api.db import get_session

router = APIRouter()


class TopologyLevel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    level: int | None = Field(
        ge=0,
        description="""A number representing the hierarchy of this resource topology in
          relation to the other resource types. These levels **shall** include a
        sequential set of positive integers starting at 0.""",
    )


class TopologyLevelsResponse(BaseModel):
    topology_levels: Sequence[TopologyLevel]


@router.get(
    "/topology-levels",
    summary="TOPOLOGY DESCRIPTION",
)
async def get_topology_levels(
    session: Session = Depends(get_session),
) -> TopologyLevelsResponse:
    result = session.execute(select(TopologyLevel))
    topology_levels = result.scalars().all()
    return TopologyLevelsResponse(topology_levels=topology_levels)


class FuelSourceType(SQLModel, table=True):
    name: str = Field(primary_key=True)
    external_id: str


class FuelSourceMetadata(SQLModel, table=True):
    external_reference: str = Field(primary_key=True)
    external_reference_url: str


class FuelSourceTypesResponse(SQLModel):
    external_reference: str | None
    external_reference_url: str | None
    types: list[FuelSourceType]


@router.get(
    "/fuel-source-types",
    summary="FUEL SOURCE TYPES",
)
async def get_fuel_source_types(
    session: Session = Depends(get_session),
) -> FuelSourceTypesResponse:
    fuel_types = session.execute(select(FuelSourceType))
    fuel_metadata = session.execute(select(FuelSourceMetadata))
    types = fuel_types.scalars().all()
    metadata = fuel_metadata.scalars().all()
    external_reference = metadata[0].external_reference
    external_reference_url = metadata[0].external_reference_url
    return FuelSourceTypesResponse(
        types=types,
        external_reference=external_reference,
        external_reference_url=external_reference_url,
    )


# class FuelTypeDescription(BaseModel):
#     name: str = Field(
#         description="A common name to use for the fuel type. If using AIB codes, it should be a concatenation of the three code descriptions with a dash between (i.e. 'Solar - Photovoltaic - Unspecified')."# noqa: E501
#     )
#     external_id: str = Field(
#         description="A unique code (such as the AIB code) referencing the type of fuel. # noqa: E501"
#     )


# class FuelTypesResponse(BaseModel):
#     external_reference: str = Field(
#         default="AIB EECS Rule Fact Sheet 5",
#         description="A reference that provides context for this specific fuel type.",
#     )
#     external_reference_url: str = Field(
#         default="https://www.aib-net.org/sites/default/files/assets/eecs/facts-sheets/AIB-2019-EECSFS-05%20EECS%20Rules%20Fact%20Sheet%2005%20-%20Types%20of%20Energy%20Inputs%20and%20Technologies%20-%20Release%207.7%20v5.pdf",# noqa: E501
#         description="A unique code (such as the AIB code) referencing the type of fuel # noqa: E501.",
#     )
#     types: list[FuelTypeDescription]
