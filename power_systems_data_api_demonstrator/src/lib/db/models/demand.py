# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class DemandModel(Base):
    """Model of grid node demand."""

    __tablename__ = "demand"

    grid_node_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float]
    unit: Mapped[str]