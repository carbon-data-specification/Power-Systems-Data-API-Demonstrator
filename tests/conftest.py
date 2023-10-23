# SPDX-License-Identifier: Apache-2.0
import os
from httpx import Client


from sqlalchemy.orm import sessionmaker
import power_systems_data_api_demonstrator.src.api.db
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel

from power_systems_data_api_demonstrator.settings import settings
from power_systems_data_api_demonstrator.src.application import get_app
import tempfile


@pytest.fixture
def session():
    temp_dir = tempfile.TemporaryDirectory()
    temp_file = os.path.join(temp_dir.name, "pytest_db.sqlite3")
    mock_engine = create_engine(f"sqlite:///{temp_file}")

    SQLModel.metadata.create_all(bind=mock_engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mock_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        temp_dir.cleanup()


@pytest.fixture
def fastapi_app(session) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()

    application.dependency_overrides[
        power_systems_data_api_demonstrator.src.api.db.get_session
    ] = lambda: session
    return application  # noqa: WPS331


@pytest.fixture
def fastapi_client(fastapi_app: FastAPI):
    return TestClient(fastapi_app, base_url="http://test")
