# SPDX-License-Identifier: Apache-2.0

from fastapi.routing import APIRouter

from power_systems_data_api_demonstrator.src.api import docs, grid_node, monitoring

api_router = APIRouter()
api_router.include_router(grid_node.router, prefix="/api", tags=["grid data"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(docs.router)
