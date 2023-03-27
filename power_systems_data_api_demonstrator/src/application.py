# SPDX-License-Identifier: Apache-2.0

from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from power_systems_data_api_demonstrator.src.api import docs, grid_node
from power_systems_data_api_demonstrator.src.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.
    This is the main constructor of an application.
    :return: application.
    """
    app = FastAPI(
        title="power_systems_data_api_demonstrator",
        version=metadata.version("power_systems_data_api_demonstrator"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(docs.router)
    # Main router for the API.
    app.include_router(grid_node.router, tags=["gridNode"])
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    return app
