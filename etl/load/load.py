import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.types import String, Float

load_dotenv(dotenv_path="./.env.dev")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SCHEMA = os.getenv("DB_SCHEMA")

lines = "data/processed/lines.csv"
stations = "data/processed/stations.csv"
static_crowding = "data/processed/static_crowding.csv"


# connect to database
def get_db_connection():
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    connection = engine.connect()
    print(f"Connected to {DB_NAME}")
    return connection


# load csv files into database
def load_to_db(file, table_name, dtype):
    df = pd.read_csv(file)
    with get_db_connection() as conn:
        engine = conn.engine
        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False,
            schema=DB_SCHEMA,
            dtype=dtype)
        print(f"loaded {table_name} into {DB_SCHEMA}")


def fetch_db_data(query):
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)


def run_load():
    load_to_db(lines, "nav_lines", dtype={
        "id": String(30),
        "name": String(50),
        "mode": String(20)
        })
    load_to_db(stations, "nav_stations", dtype={
        "id": String(30),
        "name": String(50),
        "mode": String(20),
        "lat": Float(),
        "lon": Float(),
        "live_crowding_percentage": Float()
        })
    load_to_db(static_crowding, "nav_static_crowding", dtype={
        "station_id": String(30),
        "day_of_week": String(10),
        "time_band": String(20),
        "avg_crowding_percentage": Float()
        })
