import pytest
import pandas as pd
from unittest.mock import patch
from etl.extract.api_requests import (
    get_lines,
    get_all_stations,
    get_station_static_crowding_data,
    get_all_static_crowding_data,
    get_all_live_crowding_data,
)


# test parameters
@pytest.fixture
def test_config():
    return {
        "url": "https://example.com",
        "params": {'app_key': 'test_key'},
        "endpoint": "test/endpoint",
        "station_id": "station_id",
        "station_naptan_df": pd.DataFrame({
            "stationNaptan": ["dayOfWeek", "MON"]
        }),
        "lines_response": [{"id": "line_id", "name": "line_name"}],
        "stations_response": {
            "stopPoints": [{
                "stopType": "NaptanMetroStation",
                "id": "station_id"
            }]
        },
        "crowding_response": {
            "daysOfWeek": [
                {
                    "dayOfWeek": "MON",
                    "timeBands": [{
                        "timeBand": "08:00",
                        "percentageOfCrowding": 0.5
                    }]
                }
            ]
        },
        "live_crowding_response": {"percentageOfBaseline": 0.4}
    }


# Test get_lines
@patch("etl.extract.api_requests.request_to_api")
@patch("etl.extract.api_requests.dataframe_to_csv")
def test_get_lines(mock_save, mock_api, test_config):
    mock_api.return_value = test_config["lines_response"]
    get_lines(
        test_config["url"],
        test_config["endpoint"],
        test_config["params"]
        )
    mock_api.assert_called_once()
    mock_save.assert_called_once()


# testing get_all_stations with patch
@patch("etl.extract.api_requests.request_to_api")
@patch("etl.extract.api_requests.dataframe_to_csv")
def test_get_all_stations(mock_save, mock_api, test_config):
    mock_api.return_value = test_config["stations_response"]
    get_all_stations(
        test_config["url"],
        test_config["endpoint"],
        test_config["params"]
        )
    mock_api.assert_called_once()
    mock_save.assert_called_once()


# testing get_station_static_crowding_data() for one station
@patch("etl.extract.api_requests.request_to_api")
def test_get_station_static_crowding_data(mock_request, test_config):
    mock_request.return_value = test_config["crowding_response"]
    df = get_station_static_crowding_data(
        test_config["url"],
        test_config["endpoint"],
        test_config["station_id"],
        test_config["params"]
    )
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "stationId" in df.columns


# testing get_all_static_crowding_data() for all stations
@patch("etl.extract.api_requests.pd.read_csv")
@patch("etl.extract.api_requests.get_station_static_crowding_data")
@patch("etl.extract.api_requests.dataframe_to_csv")
def test_get_all_static_crowding_data(
        mock_csv, mock_static, mock_save, test_config):
    mock_csv.return_value = test_config["station_naptan_df"]
    mock_static.return_value = pd.DataFrame([{
        "stationId": "123", "dayOfWeek": "MON"
    }])
    get_all_static_crowding_data(
        test_config["url"],
        test_config["endpoint"],
        test_config["params"]
    )
    assert mock_static.call_count == 2
    mock_save.assert_called_once()


# testing get_all_live_crowding_data()
@patch("etl.extract.api_requests.pd.read_csv")
@patch("etl.extract.api_requests.request_to_api")
@patch("etl.extract.api_requests.dataframe_to_csv")
def test_get_all_live_crowding_data(
        mock_csv, mock_request, mock_save, test_config):
    mock_csv.return_value = test_config["station_naptan_df"]
    mock_request.return_value = test_config["live_crowding_response"]

    get_all_live_crowding_data(
        test_config["url"],
        test_config["endpoint"],
        test_config["params"]
    )
    assert mock_request.call_count == 2
    mock_save.assert_called_once()
