# SPDX-License-Identifier: Apache-2.0


import pytest
from httpx import AsyncClient


async def test_health(fastapi_client: AsyncClient) -> None:
    """
    Tests that health route works.

    :param fastapi_app: current application.
    :param client: clien for the app.
    """
    response = await fastapi_client.get(
        url="/monitoring/health",
    )
    assert response.is_success


async def test_grid_nodes(fastapi_client: AsyncClient) -> None:
    """
    Tests that health route works.

    :param fastapi_app: current application.
    :param client: clien for the app.
    """
    response = await fastapi_client.get(
        url="/api/list",
    )
    assert response.is_success
    assert response.json()


@pytest.mark.parametrize("grid_node_id", [("US-WECC-CISO"), ("UK-GB"), ("ES")])
async def test_generation(fastapi_client: AsyncClient, grid_node_id: str) -> None:
    response = await fastapi_client.get(
        url=f"/api/generation/{grid_node_id}",
    )
    assert response.is_success
    assert response.json()


@pytest.mark.parametrize("grid_node_id", [("US-WECC-CISO"), ("UK-GB"), ("ES")])
async def test_demand(fastapi_client: AsyncClient, grid_node_id: str) -> None:
    response = await fastapi_client.get(
        url=f"/api/demand/{grid_node_id}",
    )
    assert response.is_success
