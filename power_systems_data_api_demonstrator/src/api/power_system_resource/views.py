# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from typing import Any, List, cast

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from power_systems_data_api_demonstrator.src.api.power_system_resource.schema import (
    CapacityDTO,
    DayAheadPriceDTO,
    DemandDTO,
    ExchangeDTO,
    FuelTypes,
    GridTopologyLevel,
    PowerSystemResourceDTO,
)
from power_systems_data_api_demonstrator.src.lib.db.dao.power_system_resource_dao import (
    GenerationDTO,
    PsrDAO,
    PsrNotFoundError,
)
from power_systems_data_api_demonstrator.src.lib.db.models.demand import DemandModel
from power_systems_data_api_demonstrator.src.lib.db.models.exchanges import (
    ExchangeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.power_system_resource_model import (
    PsrModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.prices import (
    DayAheadPriceModel,
)

router = APIRouter()


@router.get(
    "/list",
    response_model=List[PowerSystemResourceDTO],
    summary="List all available power system resources",
)
async def list_power_system_resources(
    limit: int = 10,
    power_system_resource_dao: PsrDAO = Depends(),
) -> List[PsrModel]:
    return await power_system_resource_dao.get_all_power_system_resources(limit=limit)


@router.get(
    "/describe/{id}",
    response_model=PowerSystemResourceDTO,
    summary="Describe a given power system resource",
)
async def describe_power_system_resources(
    id: str,
    power_system_resource_dao: PsrDAO = Depends(),
) -> PowerSystemResourceDTO:
    try:
        power_system_resource = await power_system_resource_dao.get_by_id(id)
        children_nodes = (
            await power_system_resource_dao.get_power_system_resource_with_parent_id(id)
        )
        # cast str power_system_resource.type to enum member PsrTopologyLevel
        return PowerSystemResourceDTO(
            id=power_system_resource.id,
            name=power_system_resource.name,
            type=cast(GridTopologyLevel, power_system_resource.type),
            parent_id=power_system_resource.parent_id,
            children_ids=[c.id for c in children_nodes],
        )

    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get(
    "/capacity/{id}",
    response_model=list[CapacityDTO],
    summary="Get installed generation capacity for a power system resource",
)
async def get_capacity_power_system_resource(
    id: str,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    power_system_resource_dao: PsrDAO = Depends(),
) -> list[CapacityDTO]:
    try:
        raw_capacities = await power_system_resource_dao.get_capacity(id)
        capacity = []
        # Filter by datetime
        dts = list(
            set([(cap.start_datetime, cap.end_datetime) for cap in raw_capacities])
        )
        if start_datetime is not None:
            dts = [dt for dt in dts if dt[0] >= start_datetime]
        if end_datetime is not None:
            dts = [dt for dt in dts if dt[0] <= end_datetime]
        # This is error prone if we don't have all fuel types for all datetimes
        # Or with different units
        for start_dt, end_dt in dts:
            capacities = [
                cap for cap in raw_capacities if cap.start_datetime == start_dt
            ]
            capacity.append(
                CapacityDTO(
                    power_system_resource_id=id,
                    start_datetime=start_dt,
                    end_datetime=end_dt,
                    generation_capacity={
                        cast(FuelTypes, cap.fuel_type): cap.value for cap in capacities
                    },
                    unit=capacities[0].unit,
                )
            )
        return capacity
    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


def filter_obs_by_datetime(
    objs: List[Any], start_datetime: datetime | None, end_datetime: datetime | None
) -> List[Any]:
    assert all([hasattr(obj, "start_datetime") for obj in objs])
    assert all([isinstance(obj.start_datetime, datetime) for obj in objs])
    dts = list(set([obj.start_datetime for obj in objs]))
    if start_datetime is not None:
        dts = [dt for dt in dts if dt >= start_datetime]
    if end_datetime is not None:
        dts = [dt for dt in dts if dt <= end_datetime]
    return [obj for obj in objs if obj.start_datetime in dts]


@router.get(
    "/generation/{id}",
    response_model=list[GenerationDTO],
    summary="Get generation for a power system resource",
)
async def get_generation_power_system_resource(
    id: str,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    power_system_resource_dao: PsrDAO = Depends(),
) -> list[GenerationDTO]:
    try:
        generation = await power_system_resource_dao.get_generation(id)
        return filter_obs_by_datetime(generation, start_datetime, end_datetime)
    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get(
    "/demand/{id}",
    response_model=list[DemandDTO],
    summary="Get demand for a power system resource",
)
async def get_demand_power_system_resource(
    id: str,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    power_system_resource_dao: PsrDAO = Depends(),
) -> list[DemandModel]:
    try:
        demand = await power_system_resource_dao.get_demand(id)
        return filter_obs_by_datetime(demand, start_datetime, end_datetime)
    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get(
    "/dayAheadPrice/{id}",
    response_model=List[DayAheadPriceDTO],
    summary="Get day ahead price for a power system resource",
)
async def get_day_ahead_price_power_system_resource(
    id: str,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    power_system_resource_dao: PsrDAO = Depends(),
) -> List[DayAheadPriceModel]:
    try:
        prices = await power_system_resource_dao.get_day_ahead_price(id)
        return filter_obs_by_datetime(prices, start_datetime, end_datetime)
    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get(
    "/imports/{id}",
    response_model=list[ExchangeDTO],
    summary="Get imports for a power system resource",
)
async def get_imports_power_system_resource(
    id: str,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    power_system_resource_dao: PsrDAO = Depends(),
) -> list[ExchangeModel]:
    try:
        imports = await power_system_resource_dao.get_imports(id)
        return filter_obs_by_datetime(imports, start_datetime, end_datetime)
    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get(
    "/exports/{id}",
    response_model=list[ExchangeDTO],
    summary="Get exports for a power system resource",
)
async def get_exports_power_system_resource(
    id: str,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    power_system_resource_dao: PsrDAO = Depends(),
) -> list[ExchangeModel]:
    try:
        exports = await power_system_resource_dao.get_exports(id)
        return filter_obs_by_datetime(exports, start_datetime, end_datetime)
    except PsrNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None
