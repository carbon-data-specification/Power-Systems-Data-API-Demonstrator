from datetime import datetime
import os
import pandas as pd
from sqlmodel import Session
from sqlmodel import SQLModel
from power_systems_data_api_demonstrator.src.api.metadata.views import TopologyLevel
from power_systems_data_api_demonstrator.src.api.psr_timeseries.views import (
    GenerationByFuelSourceTable,
    FuelType,
    FuelTechnology,
)
from power_systems_data_api_demonstrator.src.api.db import init_db
import power_systems_data_api_demonstrator.data

DATA_DIR = os.path.dirname(power_systems_data_api_demonstrator.data.__file__)


def seed() -> None:
    engine = init_db()
    topology_levels = [
        TopologyLevel(id="Level 1", level=1),
        TopologyLevel(id="Level 2", level=2),
    ]

    with Session(engine) as session:
        seed_generation(session)
        session.add_all(topology_levels)
        session.commit()


def seed_generation(session: Session) -> None:
    # Overall generation
    fuel_types = []
    fuel_technologies = []
    generation_by_fuel_source = []

    for grid_source in ["EIA", "ELEXON"]:
        df_generation = pd.read_csv(
            os.path.join(DATA_DIR, grid_source, "generation.csv")
        )
        for power_system_resource_id in df_generation["Grid Node"].unique():
            df_this_nodes_generation = df_generation[
                df_generation["Grid Node"] == power_system_resource_id
            ]
            df_generation_rows = pd.melt(
                df_this_nodes_generation,
                id_vars=["Grid Node", "start_datetime", "end_datetime", "unit"],
                var_name="fuel_type",
                value_name="value",
            ).reset_index()

            fuel_types.extend(
                [
                    FuelType(name=fuel_type, id=fuel_type)
                    for fuel_type in df_generation_rows["fuel_type"].unique().tolist()
                ]
            )

            generation_by_fuel_source.extend(
                [
                    GenerationByFuelSourceTable(
                        start_datetime=row["start_datetime"],
                        end_datetime=row["end_datetime"],
                        type=row["fuel_type"],
                        technology=None,
                        unit=row["unit"],
                        value=row["value"],
                        id=f"{grid_source}-{power_system_resource_id}",
                    )
                    for _, row in df_generation_rows.iterrows()
                ]
            )

        """
        # Generation per unit
        # Find pattern generation-*.csv
        for file in os.listdir(os.path.join(DATA_DIR, grid_source)):
            if file.startswith("generation_") and file.endswith(".csv"):
                df_generation = pd.read_csv(os.path.join(DATA_DIR, grid_source, file))
                breakpoint()
        """

    session.add_all(list(set(fuel_types)))
    session.add_all(generation_by_fuel_source)
    session.commit()
