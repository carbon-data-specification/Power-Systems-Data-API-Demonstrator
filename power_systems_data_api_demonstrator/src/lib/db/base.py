# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.orm import DeclarativeBase

from power_systems_data_api_demonstrator.src.lib.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
