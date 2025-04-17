import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from src.models.api_client import CheckWXClient

load_dotenv()


def test_init_with_api_key_from_env():
    key = os.getenv("CHECK_WX_API")
    assert key is not None, "CHECK_WX_API not found in .env"

    client = CheckWXClient()
    assert client.api_key == key


@patch.dict(os.environ, {}, clear=True)
def test_init_without_api_key_raises_error():
    with pytest.raises(EnvironmentError, match="CHECK_WX_API key is missing"):
        CheckWXClient()


@patch("requests.get")
def test_get_metar_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"icao": "EGLL"}]}
    mock_get.return_value = mock_response

    load_dotenv()
    client = CheckWXClient()
    result = client.get_metar("EGLL")

    mock_get.assert_called_once_with(
        "https://api.checkwx.com/metar/EGLL/decoded",
        headers={"X-API-Key": client.api_key},
    )
    assert result == {"data": [{"icao": "EGLL"}]}


@patch("requests.get")
def test_get_metar_error_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    load_dotenv()
    client = CheckWXClient()

    with pytest.raises(
        ValueError, match="Error retrieving data for EGLL:404 - Not Found"
    ):
        client.get_metar("EGLL")
