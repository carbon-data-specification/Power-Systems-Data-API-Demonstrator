# SPDX-License-Identifier: Apache-2.0

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class PsrModel(Base):
    """Model of a grid node."""

    __tablename__ = "power_system_resource"

    id: Mapped[str] = mapped_column(primary_key=True)
    parent_id: Mapped[str] = mapped_column(
        ForeignKey("power_system_resource.id"), nullable=True
    )
    children = relationship("PsrModel")
    name: Mapped[str]
    type: Mapped[str]
