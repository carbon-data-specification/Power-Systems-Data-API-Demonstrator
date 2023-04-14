# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class FuelTypeModel(Base):
    """Model of a grid node."""

    __tablename__ = "fuel_type"

    name: Mapped[str] = mapped_column(primary_key=True)
