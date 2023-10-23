# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
import pytest
from sqlmodel import Session
from httpx import Client
from power_systems_data_api_demonstrator.src.api.metadata.views import TopologyLevel
from power_systems_data_api_demonstrator.src.api.psr_timeseries.views import (
    GenerationByFuelSourceTable,
    FuelType,
    FuelTechnology,
)


@pytest.fixture
def _seed(session) -> None:
    topology_levels = [
        TopologyLevel(id="Level 1", level=1),
        TopologyLevel(id="Level 2", level=2),
        # Add more records as needed
    ]

    fuel_types = [FuelType(name="solar", external_id="1234")]
    fuel_technologies = [FuelTechnology(name="PV", external_id="5678")]
    generation = [
        GenerationByFuelSourceTable(
            start_datetime=datetime(2021, 1, 1),
            end_datetime=datetime(2021, 1, 1, 1),
            type="solar",
            technology="PV",
            unit="MWh",
            value=100,
            id="TEST-SOLAR-PV1",
        ),
        GenerationByFuelSourceTable(
            start_datetime=datetime(2021, 1, 1),
            end_datetime=datetime(2021, 1, 1, 1),
            type="solar",
            technology="PV2",
            unit="MWh",
            value=200,
            id="TEST-SOLAR-PV2",
        ),
    ]
    session.add_all(topology_levels)
    session.add_all(fuel_types)
    session.add_all(fuel_technologies)
    session.add_all(generation)
    session.commit()


async def test_generation(fastapi_client: Client, _seed) -> None:
    grid_node_id = "TEST-SOLAR-PV2"
    response = fastapi_client.get(
        url=f"/power-systems-resource/{grid_node_id}/timeseries/generation",
    )
    assert response.is_success
    assert response.json()
