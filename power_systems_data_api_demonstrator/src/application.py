# SPDX-License-Identifier: Apache-2.0

from importlib import metadata
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from power_systems_data_api_demonstrator.src.api.router import api_router
from power_systems_data_api_demonstrator.static.docs.utils import (
    get_app_description,
    get_app_title,
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

    # Main router for the API.
    app.include_router(api_router)
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    def custom_openapi() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=get_app_title(),
            version=metadata.version("power_systems_data_api_demonstrator"),
            description=get_app_description(),
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore

    return app
