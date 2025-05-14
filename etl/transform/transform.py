from etl.transform.transform_functions import (
    transform_all_lines,
    transform_static_crowding,
    merge_stations_live_crowding
)

# get raw data file paths
raw_lines = "data/raw/all_lines.csv"
raw_stations = "data/raw/all_stations.csv"
raw_static_crowding = "data/raw/static_crowding_data.csv"
raw_live_crowding = "data/raw/live_crowding_data.csv"


# transform
def transform_data():
    transform_all_lines(raw_lines)
    transform_static_crowding(raw_static_crowding)
    merge_stations_live_crowding(
        stations_file=raw_stations,
        live_crowding_file=raw_live_crowding
        )
