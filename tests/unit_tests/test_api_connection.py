import pytest
from unittest.mock import patch
from etl.extract.extract import request_to_api


TEST_URL = "https://example.com"
TEST_PARAMS = {'app_id': 'test_id', 'app_key': 'test_key'}


def test_request_to_api(url=TEST_URL, params=TEST_PARAMS):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        request_to_api(url, params=params)
        mock_get.assert_called_with(
            url,
            params=params)

def test_