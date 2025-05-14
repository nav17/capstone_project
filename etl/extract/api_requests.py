import requests
import pandas as pd
import time
import re


# API request function
def request_to_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        print("Error message:", response.content)


# Save API response to csv
def response_to_dataframe(data, normalize=False):
    if normalize:
        return pd.json_normalize(data)
    return pd.DataFrame(data)


# Save API response to csv
def raw_dataframe_to_csv(df, filename):
    df.to_csv(f"data/raw/{filename}.csv")
    print(f"Raw data saved to data/{filename}.csv")
    return df


# Get tube & elizabeth lines
def get_lines(base_url, endpoint, params):
    print("collecting lines...")
    data = request_to_api(url=base_url+endpoint, params=params)
    print("lines collected!")
    df = response_to_dataframe(data)
    raw_dataframe_to_csv(df, "all_lines")


# Get all stations
def get_all_stations(base_url, endpoint, params):
    print("collecting stations...")
    data = request_to_api(url=base_url+endpoint, params=params)
    print("stations collected!")
    df = response_to_dataframe(data["stopPoints"], normalize=True)
    # Only save stations
    df = df[df["stopType"].isin(["NaptanMetroStation", "NaptanRailStation"])]
    raw_dataframe_to_csv(df, "all_stations")


# CROWDING DATA:
# Get static crowding data for a given station
def get_station_static_crowding_data(base_url, endpoint, station_id, params):
    data = request_to_api(url=base_url+endpoint+station_id, params=params)
    time_bands = []
    for day in data["daysOfWeek"]:
        day_of_week = day["dayOfWeek"]
        for time_band in day["timeBands"]:
            time_band["stationId"] = station_id
            time_band["dayOfWeek"] = day_of_week
            time_bands.append(time_band)
    df = pd.DataFrame(time_bands)
    return df


# Get static crowding data for all stations
def get_all_static_crowding_data(base_url, endpoint, params):
    stations = pd.read_csv("data/raw/all_stations.csv")
    print("loaded stations")
    dfs = []
    i = 0
    for station_id in stations["stationNaptan"]:
        i += 1
        extracted = False
        while not extracted:
            try:
                print(f"Processing static crowding: {i}/{len(stations)}")
                df = get_station_static_crowding_data(
                    base_url=base_url,
                    endpoint=endpoint,
                    params=params,
                    station_id=station_id
                )
                dfs.append(df)
                time.sleep(1)
                extracted = True
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    error_message = e.response.text
                    wait_time_search = re.search(
                        r"in ([0-9]+) seconds", error_message)
                    wait_time = int(wait_time_search.group(1))
                    print(f"hit rate limit, sleeping for {wait_time}")
                    time.sleep(wait_time)
                else:
                    print("HTTP error: ", e.response.status_code)
            except Exception as e:
                print(f"Failed for {station_id}: {e}")
    print("all static crowding collected")
    crowding_df = pd.concat(dfs)
    raw_dataframe_to_csv(crowding_df, "static_crowding_data")


# Get live crowding data for all stations
def get_all_live_crowding_data(base_url, endpoint, params):
    stations = pd.read_csv("data/raw/all_stations.csv")
    print("loaded stations")
    all_live_crowding = []
    skipped = 0
    i = 0
    for station_id in stations["stationNaptan"]:
        i += 1
        extracted = False
        while not extracted:
            try:
                print(f"Processing live crowding: {i}/{len(stations)}")
                data = request_to_api(
                    url=base_url+endpoint+station_id+"/Live",
                    params=params
                    )
                if data.get("dataAvailable", False):
                    station_live_crowding = {
                        "stationId": station_id,
                        "live_crowding_percentage":
                            data['percentageOfBaseline'],
                        "dataAvailable": data['dataAvailable'],
                        "timeLocal": data['timeLocal']
                    }
                    all_live_crowding.append(station_live_crowding)
                else:
                    skipped += 1
                time.sleep(1)
                extracted = True
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    error_message = e.response.text
                    wait_time_search = re.search(
                        r"in ([0-9]+) seconds", error_message)
                    wait_time = int(wait_time_search.group(1))
                    print(f"hit rate limit, sleeping for {wait_time}")
                    time.sleep(wait_time)
                else:
                    print("HTTP error: ", e.response.status_code)
            except Exception as e:
                print(f"Failed for {station_id}: {e}")
    print("all live crowding collected")
    print(f"skipped {skipped} stations due to unavailable data")
    crowding_df = pd.DataFrame(all_live_crowding)
    raw_dataframe_to_csv(crowding_df, "live_crowding_data")


# # Additional functions:
# # DELAY DATA:
# 5. get_all_delays (line_id, severity, reason)
# DEPARTURE/ARRIVAL BOARDS
# 6. get_arrivals gets arrivals for each line on each station
# ROUTE DATA:
# 7. get_all_routes (line_id, origin, destination, direction, route stations)
