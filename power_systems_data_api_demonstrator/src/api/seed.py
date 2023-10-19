from power_systems_data_api_demonstrator.src.api.db import engine
from sqlmodel import Session
from sqlmodel import SQLModel
from power_systems_data_api_demonstrator.src.api.metadata.views import TopologyLevel
from power_systems_data_api_demonstrator.src.api.db import init_db


def seed() -> None:
    init_db()
    topology_levels = [
        TopologyLevel(id="Level 1", level=1),
        TopologyLevel(id="Level 2", level=2),
        # Add more records as needed
    ]
    with Session(engine) as session:
        session.add_all(topology_levels)
        session.commit()
