from fastapi.routing import APIRouter

from power_systems_data_api_demonstrator.web.api import (
    docs,
    grid_node,
    monitoring,
)

api_router = APIRouter()
api_router.include_router(grid_node.router, prefix="/gridNode", tags=["gridNode"])
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
