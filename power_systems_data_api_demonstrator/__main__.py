# SPDX-License-Identifier: Apache-2.0

import uvicorn

from power_systems_data_api_demonstrator.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "power_systems_data_api_demonstrator.src.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
