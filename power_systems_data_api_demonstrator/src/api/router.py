# SPDX-License-Identifier: Apache-2.0

from fastapi.routing import APIRouter

from power_systems_data_api_demonstrator.src.api import docs
from power_systems_data_api_demonstrator.src.api.db import init_db
from power_systems_data_api_demonstrator.src.api.metadata.views import (
    router as metadata_router,
)
from power_systems_data_api_demonstrator.src.api.psr_metadata.views import (
    router as psr_metadata_router,
)
from power_systems_data_api_demonstrator.src.api.psr_timeseries.views import (
    router as psr_timeseries_router,
)
from power_systems_data_api_demonstrator.src.api.seed import seed

api_router = APIRouter()
api_router.include_router(metadata_router, prefix="/metadata", tags=["metadata"])
api_router.include_router(
    psr_metadata_router, prefix="/power-systems-resource", tags=["psr metadata"]
)
api_router.include_router(
    psr_timeseries_router, prefix="/power-systems-resource", tags=["psr timeseries"]
)
api_router.include_router(docs.router)


@api_router.on_event("startup")
def startup_event() -> None:
    seed()
