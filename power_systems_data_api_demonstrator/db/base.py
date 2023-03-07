from sqlalchemy.orm import DeclarativeBase

from power_systems_data_api_demonstrator.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
