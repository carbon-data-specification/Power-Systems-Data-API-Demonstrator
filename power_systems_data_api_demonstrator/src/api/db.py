import os

from sqlmodel import Session, SQLModel, create_engine
from power_systems_data_api_demonstrator.settings import settings


def get_engine():
    return create_engine(str(settings.db_url), echo=False)


def init_db():
    engine = get_engine()
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    return engine


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
