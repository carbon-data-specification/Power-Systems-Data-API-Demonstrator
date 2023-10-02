# SPDX-License-Identifier: Apache-2.0

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class DayAheadPriceModel(Base):
    """Model of day ahead price for a node."""

    __tablename__ = "day_ahead_price"

    power_system_resource_id: Mapped[str] = mapped_column(
        ForeignKey("power_system_resource.id"), primary_key=True
    )
    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float]
    currency: Mapped[str]
