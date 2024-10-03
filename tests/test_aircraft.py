import pytest
import os
import json
from unittest.mock import patch
from src.models.aircraft import Aircraft


def test_load_json_aircraft_data():
    aircraft_icao = "b738"
    file_path = f"src/aircraft_data/json_data/boeing/{aircraft_icao}/__init__.json"

    if not os.path.exists(file_path):
        pytest.fail(f"Test data file does not exist: {file_path}")

    aircraft = Aircraft(aircraft_icao)

    with open(file_path, "r") as f:
        expected_data = json.load(f)

    assert aircraft.data == expected_data


@patch("os.path.exists", return_value=False)
def test_file_not_found(mock_exists):
    icao = "b738"
    with pytest.raises(
        ValueError, match=f"No data found for aircraft ICAO: {icao}"
    ):
        Aircraft(icao)


def test_manufacturer_not_found():
    icao = "x123"
    with pytest.raises(
        ValueError, match=f"Manufacturer not found for aircraft ICAO: {icao}"
    ):
        Aircraft(icao)


def test_empty_icao_code():
    with pytest.raises(ValueError, match="ICAO code cannot be empty."):
        Aircraft("")
