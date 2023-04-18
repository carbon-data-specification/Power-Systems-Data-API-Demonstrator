# SPDX-License-Identifier: Apache-2.0

from fastapi import APIRouter, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse, RedirectResponse

from power_systems_data_api_demonstrator.static.docs.utils import get_app_title

router = APIRouter()


@router.get("/", include_in_schema=False)
async def redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/docs", include_in_schema=False)
async def swagger_ui_html(request: Request) -> HTMLResponse:
    """
    Swagger UI.

    :param request: current request.
    :return: rendered swagger UI.
    """
    return get_swagger_ui_html(
        openapi_url=request.app.openapi_url,
        title=get_app_title(),
        oauth2_redirect_url=request.url_for("swagger_ui_redirect"),
        swagger_js_url="/static/docs/swagger-ui-bundle.js",
        swagger_css_url="/static/docs/swagger-ui.css",
    )


@router.get("/swagger-redirect", include_in_schema=False)
async def swagger_ui_redirect() -> HTMLResponse:
    """
    Redirect to swagger.

    :return: redirect.
    """
    return get_swagger_ui_oauth2_redirect_html()


@router.get("/redoc", include_in_schema=False)
async def redoc_html(request: Request) -> HTMLResponse:
    """
    Redoc UI.

    :param request: current request.
    :return: rendered redoc UI.
    """
    return get_redoc_html(
        openapi_url=request.app.openapi_url,
        title=get_app_title(),
        redoc_js_url="/static/docs/redoc.standalone.js",
    )
