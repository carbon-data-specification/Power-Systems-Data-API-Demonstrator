# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class ExchangeModel(Base):
    """Model of grid node generation for a given fuel type."""

    __tablename__ = "exchanges"

    power_system_resource_from_id: Mapped[str] = mapped_column(
        ForeignKey("power_system_resource.id"), primary_key=True
    )
    power_system_resource_to_id: Mapped[str] = mapped_column(
        ForeignKey("power_system_resource.id"), primary_key=True
    )
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float]
    unit: Mapped[str]
