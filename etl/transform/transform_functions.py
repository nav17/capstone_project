import pandas as pd

# line colors sourced from
# https://content.tfl.gov.uk/tfl-basic-elements-standards-issue-08.pdf
line_colors = {
    "elizabeth": "#753BBD",
    "bakerloo": "#A45A2A",
    "central": "#DA291C",
    "circle": "#FFCD00",
    "district": "#007A33",
    "hammersmith-city": "#E89CAE",
    "jubilee": "#7C878E",
    "metropolitan": "#840B55",
    "northern": "#000000",
    "piccadilly": "#10069F",
    "victoria": "#00A3E0",
    "waterloo-city": "#6ECEB2",
}


# save processed dataframe to csv
def transformed_dataframe_to_csv(df, filename, index=False):
    df.to_csv(f"data/processed/{filename}.csv", index=index)
    print(f"Processed data saved to data/{filename}.csv")
    return df


# transform lines data
def transform_all_lines(file):
    df = pd.read_csv(file)
    df = df[["id", "name", "modeName"]]
    df.columns = ["id", "name", "mode"]
    df["line_colour"] = df["id"].map(line_colors)
    transformed_dataframe_to_csv(df, "lines")


# filter modes in all_stations
def filter_modes(mode):
    modes = mode.strip("[]").replace("'", "").split(",")
    for m in modes:
        m = m.strip()
        if m == "tube":
            return "tube"
        elif m == "elizabeth-line":
            return "elizabeth-line"
    return None


# transform stations data
def transform_all_stations(file):
    df = pd.read_csv(file)
    df = df[["stationNaptan", "commonName", "modes", "lat", "lon"]]
    df["modes"] = df["modes"].apply(filter_modes)
    df.columns = ["station_id", "name", "mode", "lat", "lon"]
    return df


# transform static crowding data
def transform_static_crowding(file):
    df = pd.read_csv(file)
    df = df[["stationId", "dayOfWeek", "timeBand", "percentageOfBaseLine"]]
    df.columns = [
        "id", "day_of_week", "time_band", "avg_crowding_percentage"]
    df["avg_crowding_percentage"] = (
        df["avg_crowding_percentage"] * 100).round(2)
    transformed_dataframe_to_csv(df, "static_crowding")


# transform live crowding data
def transform_live_crowding(file):
    df = pd.read_csv(file)
    df = df[["stationId", "live_crowding_percentage"]]
    df.columns = ["station_id", "live_crowding_percentage"]
    df["live_crowding_percentage"] = (
        df["live_crowding_percentage"] * 100).round(2)
    return df


# merge stations and live crowding data
def merge_stations_live_crowding(stations_file, live_crowding_file):
    stations = transform_all_stations(stations_file)
    live_crowding = transform_live_crowding(live_crowding_file)
    merged_df = pd.merge(stations, live_crowding, on="station_id")
    merged_df.rename(columns={"station_id": "id"}, inplace=True)
    transformed_dataframe_to_csv(merged_df, "stations")
