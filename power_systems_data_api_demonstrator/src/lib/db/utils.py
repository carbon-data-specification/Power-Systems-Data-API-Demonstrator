# SPDX-License-Identifier: Apache-2.0

import os

from power_systems_data_api_demonstrator.settings import settings


async def create_database() -> None:
    """Create a databse."""


async def drop_database() -> None:
    """Drop current database."""
    if settings.db_file.exists():
        os.remove(settings.db_file)
