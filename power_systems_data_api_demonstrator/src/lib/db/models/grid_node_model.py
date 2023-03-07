from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class GridNodeModel(Base):
    """Model of a grid node."""

    __tablename__ = "grid_node"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]


class GenerationModel(Base):
    """Model of grid node generation."""

    __tablename__ = "generation"

    grid_node_id: Mapped[str] = mapped_column(
        ForeignKey("grid_node.id"), primary_key=True
    )
    datetime_utc: Mapped[datetime]
    energy: Mapped[float]
    unit: Mapped[str]
