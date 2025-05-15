import os
from etl.extract.api_requests import (
    get_lines,
    get_all_stations,
    get_all_static_crowding_data,
    get_all_live_crowding_data,
    # get_all_routes
    )

# Base URL for the API
base_url = "https://api.tfl.gov.uk/"

# Endpoints
tube_lines = "Line/Mode/tube,elizabeth-line"
all_stations = "StopPoint/Mode/tube"
crowding = "crowding/"
route_line = "Line/"
route_sequence = "/Route/Sequence/"

# Load API Credentials from .env
app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")

params = {
    'app_key': app_key
}


def extract_data():
    get_lines(base_url=base_url, endpoint=tube_lines, params=params)
    get_all_stations(base_url=base_url, endpoint=all_stations, params=params)

    if os.path.exists("data/raw/static_crowding_data.csv"):
        print("static crowding data loaded from cache")
    else:
        get_all_static_crowding_data(
            base_url=base_url, endpoint=crowding, params=params)

    get_all_live_crowding_data(
        base_url=base_url, endpoint=crowding, params=params)
