# SPDX-License-Identifier: Apache-2.0

from typing import Dict

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health", summary="Perform a health check")
async def perform_healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@router.get("/echo", summary="Echo a message")
@router.post("/echo", summary="Echo a message")
async def send_echo(request: Request) -> Dict[str, str]:
    try:
        json_body = await request.json()
    except Exception:
        return {"message": ""}
    return {"message": json_body.get("message", "")}
