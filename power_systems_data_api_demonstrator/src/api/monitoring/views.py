# SPDX-License-Identifier: Apache-2.0

from typing import Dict

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
async def perform_healthcheck() -> Dict[str, str]:
    """
    Perform a health check.

    :return: a dictionary with the health status.
    """
    return {"status": "ok"}


@router.get("/echo")
@router.post("/echo")
async def send_echo(request: Request) -> Dict[str, str]:
    """
    Echo a message.

    :param message: message to echo.
    :return: a dictionary with the message.
    """
    try:
        json_body = await request.json()
    except Exception:
        return {"message": ""}
    return {"message": json_body.get("message", "")}
