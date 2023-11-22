import os

import pandas as pd
from sqlmodel import Session

import power_systems_data_api_demonstrator.data
from power_systems_data_api_demonstrator.src.api.db import init_db
from power_systems_data_api_demonstrator.src.api.metadata.views import (
    FuelSourceTechnologyReferenceTable,
    FuelSourceType,
    TopologyLevel,
)
from power_systems_data_api_demonstrator.src.api.psr_metadata.views import (
    CapacityTable,
    PSRInterconnectionTable,
    PSRList,
)
from power_systems_data_api_demonstrator.src.api.psr_timeseries.views import (
    FuelType,
    GenerationByFuelSourceTable,
)

DATA_DIR = os.path.dirname(power_systems_data_api_demonstrator.data.__file__)


def seed() -> None:
    engine = init_db()

    topology_levels = []

    for grid_source in ["example"]:
        df = pd.read_csv(os.path.join(DATA_DIR, grid_source, "topology_metadata.csv"))

    levels = df

    for index, row in levels.iterrows():
        topology_levels.extend([TopologyLevel(id=row["id"], level=row["level"])])

    with Session(engine) as session:
        seed_generation(session)
        session.add_all(topology_levels)
        seed_fuelsource(session)
        seed_psr(session)
        session.commit()


def seed_fuelsource(session: Session) -> None:
    for grid_source in ["example"]:
        df = pd.read_csv(
            os.path.join(DATA_DIR, grid_source, "fuel_source_metadata.csv")
        )

    fuel_source_types = []
    fuel_source_technologies = []

    types = df[df["external_id"].str.contains("F")].reset_index()
    technologies = df[~df["external_id"].str.contains("F")].reset_index()
    for index, row in types.iterrows():
        fuel_source_types.extend(
            [
                FuelSourceType(
                    name=row["name"],
                    external_id=row["external_id"],
                    external_reference=row["external_reference"],
                )
            ]
        )

    for index, row in technologies.iterrows():
        fuel_source_technologies.extend(
            [
                FuelSourceTechnologyReferenceTable(
                    name=row["name"],
                    aibCode=row["external_id"],
                    source_document=row["external_reference"],
                )
            ]
        )

    # session.add_all(fuelsource_types)
    # session.add_all(fuelsource_technologies)
    session.add_all(fuel_source_types)
    session.add_all(fuel_source_technologies)
    session.commit()


def extract_info(df: pd.DataFrame, column_name: str):
    """
    Extracts the information from a column with a list of dicts and
     adds them as columns to the dataframe.

    Input:
    ----------
    df : pd.DataFrame
    column_name : str

    Returns
    -------
    df : pd.DataFrame
    """
    df = df.explode(column_name).reset_index(drop=True)
    extracted_info = df[column_name].apply(pd.Series).reset_index(drop=True)
    df = df.join(extracted_info)
    df = df.drop(column_name, axis=1)

    return df


def seed_psr(session: Session) -> None:
    psr_data = []
    generation_capacity = []
    transmission_capacity = []

    for grid_source in ["example"]:
        df = pd.read_json(os.path.join(DATA_DIR, grid_source, "psr_metadata.json"))
        # PSR List
        psr_data = []

        for index, row in df.iterrows():
            psr_data.extend([PSRList(id=row["id"], level=row["topology_level"])])

        # PSR GENERATION CAPACITY

        generation_capacity = []
        # select only the rows with generation capacity data
        df_generation = df.dropna(subset=["fuelSource_capacity"]).copy()
        df_generation = df_generation[["id", "fuelSource_capacity"]]
        # extract fuelSource_capacity info
        df_generation = extract_info(df_generation, "fuelSource_capacity")
        df_generation = extract_info(df_generation, "capacity")

        for index, row in df_generation.iterrows():
            print("datetime")
            print(pd.to_datetime(row["startDatetime"]))
            capacity_table = CapacityTable(
                id=row["id"],
                unit=row["unit"],
                type=row["type"],
                technology=row["technology"],
                value=row["value"],
                startDatetime=row["startDatetime"],
            )

            if not pd.isna(row["endDatetime"]):
                capacity_table.endDatetime = row["endDatetime"]

            generation_capacity.extend([capacity_table])

        # PSR TRANSMISSION CAPACITY
        transmission_capacity = []
        # select only the rows with transmission capacity data
        df_transmission = df.dropna(subset=["transmission_capacity"]).copy()
        # extract transmission_capacity info
        df_transmission = extract_info(df_transmission, "transmission_capacity")

        for index, row in df_transmission.iterrows():
            transmission_capacity.extend(
                [
                    PSRInterconnectionTable(
                        id=row["id"],
                        unit=row["unit"],
                        connectedPSR=row["connectedPSR"],
                        value=row["value"],
                    )
                ]
            )

    session.add_all(generation_capacity)
    session.add_all(psr_data)
    session.add_all(transmission_capacity)
    session.commit()


def seed_generation(session: Session) -> None:
    # Overall generation
    fuel_types = []
    # fuel_technologies = []
    generation_interconnection_by_fuel_source = []
    generation_balancing_area_by_fuel_source = []

    for grid_source in ["EIA", "ELEXON"]:
        df_generation = pd.read_csv(
            os.path.join(DATA_DIR, grid_source, "generation.csv")
        )

        # Topology Level: Parent Node
        df_by_interconnection = (
            df_generation.groupby(
                ["Parent Node", "start_datetime", "end_datetime", "unit"]
            )
            .sum(numeric_only=True)
            .reset_index()
        )
        for power_system_resource_id in df_by_interconnection["Parent Node"].unique():
            df_generation_rows = pd.melt(
                df_by_interconnection,
                id_vars=["Parent Node", "start_datetime", "end_datetime", "unit"],
                var_name="fuel_type",
                value_name="value",
            ).reset_index()

            generation_interconnection_by_fuel_source.extend(
                [
                    GenerationByFuelSourceTable(
                        start_datetime=row["start_datetime"],
                        end_datetime=row["end_datetime"],
                        type=row["fuel_type"],
                        technology=None,
                        unit=row["unit"],
                        value=row["value"],
                        id=power_system_resource_id,
                    )
                    for _, row in df_generation_rows.iterrows()
                ]
            )

            # Also add the fuel types
            fuel_types.extend(
                [
                    FuelType(name=fuel_type, id=fuel_type)
                    for fuel_type in df_generation_rows["fuel_type"].unique().tolist()
                ]
            )

        for power_system_resource_id in df_generation["Grid Node"].unique():
            print(power_system_resource_id)
            df_this_nodes_generation = df_generation[
                df_generation["Grid Node"] == power_system_resource_id
            ]
            df_generation_rows = pd.melt(
                df_this_nodes_generation,
                id_vars=[
                    "Grid Node",
                    "Parent Node",
                    "start_datetime",
                    "end_datetime",
                    "unit",
                ],
                var_name="fuel_type",
                value_name="value",
            ).reset_index()

            generation_balancing_area_by_fuel_source.extend(
                [
                    GenerationByFuelSourceTable(
                        start_datetime=row["start_datetime"],
                        end_datetime=row["end_datetime"],
                        type=row["fuel_type"],
                        technology=None,
                        unit=row["unit"],
                        value=row["value"],
                        id=power_system_resource_id,
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
    session.add_all(generation_interconnection_by_fuel_source)
    session.add_all(generation_balancing_area_by_fuel_source)
    session.commit()
