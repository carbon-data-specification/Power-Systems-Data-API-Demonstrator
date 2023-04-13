# SPDX-License-Identifier: Apache-2.0

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class GenerationForFuelTypeModel(Base):
    """Model of grid node generation for a given fuel type."""

    __tablename__ = "generation_per_fuel_type"

    grid_node_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    datetime: Mapped[datetime]
    value: Mapped[float]
    unit: Mapped[str]
    fuel_type: Mapped[str]
