import pytest
import pandas as pd
from unittest.mock import patch
from etl.extract.api_requests import (
    request_to_api,
    response_to_dataframe,
    dataframe_to_csv
)


@pytest.fixture
def test_config():
    return {
        "url": "https://example.com",
        "params": {'app_key': 'test_key'},
        "endpoint": "test/endpoint",
        "response": [{"id": "line_id", "name": "line name"}],
        "normalize_response": [{
            "id": "line_id",
            "stations": [{"name": "station", "id": "station_id"}]
        }]
    }


# testing request_to_api()
@patch('requests.get')
def test_request_to_api(mock_get, test_config):
    mock_get.return_value.status_code = 200
    request_to_api(test_config["url"], params=test_config["params"])
    mock_get.assert_called_once_with(
        test_config["url"], params=test_config["params"])


# testing response_to_dataframe() default condition
def test_response_to_dataframe(test_config):
    df = response_to_dataframe(test_config["response"])
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)


# testing response_to_dataframe(normalize=True)
def test_response_to_normalize_dataframe(test_config):
    df = response_to_dataframe(
        test_config["normalize_response"], normalize=True)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)


# testing dataframe_to_csv()
def test_dataframe_to_csv(test_config):
    df = pd.DataFrame(test_config["response"])
    returned_df = dataframe_to_csv(df, "test_file")
    assert isinstance(returned_df, pd.DataFrame)
