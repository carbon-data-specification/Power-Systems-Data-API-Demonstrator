# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class ExchangeModel(Base):
    """Model of grid node generation for a given fuel type."""

    __tablename__ = "exchanges"

    grid_node_from_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    grid_node_to_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float]
    unit: Mapped[str]
