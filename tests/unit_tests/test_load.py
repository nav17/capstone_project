import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from sqlalchemy.types import String
from etl.load.load import (
    load_to_db,
    fetch_db_data,
    get_db_connection
)


# mock dataframe
@pytest.fixture
def test_dataframe():
    return pd.DataFrame({
        "id": ["001"],
        "name": ["bakerloo"],
        "mode": ["tube"]
    })


# mock database connection
@pytest.fixture
def mock_db_conn():
    mock_conn = MagicMock()
    mock_engine = MagicMock()
    mock_engine.to_sql = MagicMock()
    mock_conn.engine = mock_engine
    return mock_conn


# chat gpt assisted with database connection testing below

# testing load_to_db()
@patch("etl.load.load.get_db_connection")
@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_sql")
def test_load_to_db(mock_to_sql, mock_read_csv, mock_get_conn, test_dataframe,
                    mock_db_conn):
    mock_read_csv.return_value = test_dataframe
    mock_get_conn.return_value.__enter__.return_value = mock_db_conn

    load_to_db("mock.csv", "test_table", dtype={
        "id": String(30),
        "name": String(50),
        "mode": String(20)
    })

    mock_read_csv.assert_called_once_with("mock.csv")
    mock_to_sql.assert_called_once()


# testing fetch_db_data()
@patch("etl.load.load.get_db_connection")
@patch("pandas.read_sql")
def test_fetch_db_data(mock_read_sql, mock_get_conn, mock_db_conn):
    mock_df = pd.DataFrame({"col": [1]})
    mock_get_conn.return_value.__enter__.return_value = mock_db_conn
    mock_read_sql.return_value = mock_df

    result = fetch_db_data("SELECT * FROM test_table")

    mock_read_sql.assert_called_once_with(
        "SELECT * FROM test_table", mock_db_conn)
    assert isinstance(result, pd.DataFrame)
    assert result.equals(mock_df)


# testing get_db_connection()
@patch("etl.load.load.create_engine")
def test_get_db_connection(mock_create_engine):
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value = mock_conn
    mock_create_engine.return_value = mock_engine

    conn = get_db_connection()

    mock_create_engine.assert_called_once()
    mock_engine.connect.assert_called_once()
    assert conn == mock_conn
