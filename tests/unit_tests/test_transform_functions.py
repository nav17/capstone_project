import pytest
import pandas as pd
from unittest.mock import patch
from etl.transform.transform_functions import (
    transformed_dataframe_to_csv,
    transform_all_lines,
    filter_modes,
    transform_all_stations,
    transform_static_crowding,
    transform_live_crowding,
    merge_stations_live_crowding
)


# chatgpt was used to generate mock data
# mock line data for testing
@pytest.fixture
def test_line_data(tmp_path):
    file = tmp_path / "lines.csv"
    df = pd.DataFrame({
        "id": ["bakerloo"],
        "name": ["Bakerloo Line"],
        "modeName": ["tube"]
    })
    df.to_csv(file, index=False)
    return file


# mock station data for testing
@pytest.fixture
def test_station_data(tmp_path):
    file = tmp_path / "all_stations.csv"
    df = pd.DataFrame({
        "stationNaptan": ["001"],
        "commonName": ["Test Station"],
        "modes": ["['tube']"],
        "lat": [51.5],
        "lon": [-0.1]
    })
    df.to_csv(file, index=False)
    return file


# mock crowding data for testing
@pytest.fixture
def test_live_crowding_data(tmp_path):
    file = tmp_path / "live_crowding.csv"
    df = pd.DataFrame({
        "stationId": ["001"],
        "live_crowding_percentage": [0.25],
        "dataAvailable": [True],
        "timeLocal": ["2025-05-15 08:11:00"]
    })
    df.to_csv(file, index=False)
    return file


# mock static crowding data for testing
@pytest.fixture
def test_static_crowding_data(tmp_path):
    file = tmp_path / "static.csv"
    df = pd.DataFrame({
        "stationId": ["001"],
        "dayOfWeek": ["MON"],
        "timeBand": ["08:00"],
        "percentageOfBaseLine": [0.3]
    })
    df.to_csv(file, index=False)
    return file


# testing transform_all_lines()
@patch("etl.transform.transform_functions.transformed_dataframe_to_csv")
def test_transform_all_lines(mock_save, test_line_data):
    transform_all_lines(test_line_data)
    mock_save.assert_called_once()


# testing filter_modes()
def test_filter_modes():
    assert filter_modes("['tube']") == "tube"
    assert filter_modes("['elizabeth-line']") == "elizabeth-line"
    assert filter_modes("['national-rail']") is None


# testing transform_all_stations()
def test_transform_all_stations(test_station_data):
    df = transform_all_stations(test_station_data)
    assert not df.empty
    assert "station_id" in df.columns


# testing transform_live_crowding()
def test_transform_live_crowding(test_live_crowding_data):
    df = transform_live_crowding(test_live_crowding_data)
    assert df["live_crowding_percentage"].iloc[0] == 25.0


# testing transform_static_crowding()
@patch("etl.transform.transform_functions.transformed_dataframe_to_csv")
def test_transform_static_crowding(mock_save, test_static_crowding_data):
    transform_static_crowding(test_static_crowding_data)
    mock_save.assert_called_once()


# testing transformed_dataframe_to_csv()
@patch("pandas.DataFrame.to_csv")
def test_transformed_dataframe_to_csv(mock_csv):
    df = pd.DataFrame({"col": [1]})
    result = transformed_dataframe_to_csv(df, "test_output", index=False)
    mock_csv.assert_called_once()
    assert isinstance(result, pd.DataFrame)


# test for merge_stations_live_crowding() written by chatgpt
@patch("etl.transform.transform_functions.transformed_dataframe_to_csv")
def test_merge_stations_live_crowding(
        mock_save, test_station_data, test_live_crowding_data):
    merge_stations_live_crowding(test_station_data, test_live_crowding_data)
    mock_save.assert_called_once()
    merged_df = mock_save.call_args[0][0]
    assert "id" in merged_df.columns
    assert "live_crowding_percentage" in merged_df.columns
