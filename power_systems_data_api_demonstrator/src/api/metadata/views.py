from typing import Optional, Sequence

import pandas as pd
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
    external_reference: Optional[str]
    external_id: Optional[str]


class FuelSourceTypesResponse(SQLModel):
    types: list[FuelSourceType]


@router.get(
    "/fuel-source/types",
    summary="FUEL SOURCE TYPES",
)
async def get_fuel_source_types(
    session: Session = Depends(get_session),
) -> FuelSourceTypesResponse:
    result = session.execute(select(FuelSourceType))
    types = result.scalars().all()
    return FuelSourceTypesResponse(types=types)


class FuelSourceTechnologyReference(SQLModel):
    aibCode: str
    source_document: str


class FuelSourceTechnologyReferenceTable(FuelSourceTechnologyReference, table=True):
    name: str = Field(primary_key=True)


class FuelSourceTechnology(SQLModel):
    name: str
    externalReference: FuelSourceTechnologyReference


class FuelSourceTechnologyResponse(SQLModel):
    technologies: Sequence[FuelSourceTechnology]


@router.get(
    "/fuel-source/technologies",
    summary="FUEL SOURCE TECHNOLOGIES",
)
async def get_fuel_source_technologies(
    session: Session = Depends(get_session),
) -> FuelSourceTechnologyResponse:
    result = session.execute(select(FuelSourceTechnologyReferenceTable))
    technologies = result.scalars().all()
    df = pd.DataFrame(g.dict() for g in technologies)
    technologies = []
    for index, row in df.iterrows():
        technologies.append(
            # FuelSourceTechnologyReferenceTable(
            FuelSourceTechnology(
                name=row["name"],
                externalReference=FuelSourceTechnologyReference(
                    aibCode=row["aibCode"],
                    source_document=row["source_document"],
                ),
            )
        )
    return FuelSourceTechnologyResponse(technologies=technologies)


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
