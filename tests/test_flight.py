import pytest
import os
import json
from src.models.flight import Flight
from unittest.mock import patch


@pytest.fixture
def valid_flight():
    return Flight("ULLI", "UUEE", "b738")


def test_save_to_json_creates_file(valid_flight):
    filename = (
        f"route-{valid_flight.aircraft.aircraft_icao}-"
        f"{valid_flight.dep_airport.icao_code}-"
        f"to-{valid_flight.arr_airport.icao_code}.json"
    )

    valid_flight.save_to_json()
    assert os.path.exists(filename)
    os.remove(filename)


def test_save_to_json_content(valid_flight):
    filename = (
        f"route-{valid_flight.aircraft.aircraft_icao}-"
        f"{valid_flight.dep_airport.icao_code}-"
        f"to-{valid_flight.arr_airport.icao_code}.json"
    )

    valid_flight.save_to_json()

    with open(filename, "r") as file:
        data = json.load(file)

    expected_data = valid_flight._to_dict()
    assert data == expected_data

    os.remove(filename)


def test_save_to_json_io_error(valid_flight):
    with patch("builtins.open", side_effect=IOError("File error")):
        with pytest.raises(
            IOError, match="Error saving JSON file: File error"
        ):
            valid_flight.save_to_json()


def test_calculate_distance_km(valid_flight):
    expected_distance = valid_flight._haversine_distance(
        valid_flight.dep_airport.latitude,
        valid_flight.dep_airport.longitude,
        valid_flight.arr_airport.latitude,
        valid_flight.arr_airport.longitude,
    )
    distance_km = valid_flight.calculate_distance_km()
    assert distance_km == pytest.approx(expected_distance, rel=1e-5)


def test_calculate_distance_km_invalid_coordinates(valid_flight):
    valid_flight.dep_airport.latitude = None
    valid_flight.dep_airport.longitude = "Not a number"

    with pytest.raises(
        ValueError,
        match="Invalid coordinates for departure or arrival airports."
    ):
        valid_flight.calculate_distance_km()


def test_calculate_block_fuel(valid_flight):
    fuel_on_100km = int(valid_flight.aircraft_data["FuelOn100km"]["MAX"])
    distance_100km = valid_flight._distance_100km()
    expected_block_fuel = fuel_on_100km * distance_100km

    block_fuel = valid_flight.calculate_block_fuel()
    assert block_fuel == expected_block_fuel


def test_calculate_payload(valid_flight):
    expected_payload = valid_flight.passengers_count * 104
    payload = valid_flight.calculate_payload()
    assert payload == expected_payload


def test_calculate_payload_passenger_count_negative_integer(valid_flight):
    valid_flight.aircraft_data["Passengers"]["MAX"] = -1
    with pytest.raises(ValueError, match="Invalid passenger count data."):
        valid_flight.calculate_payload()


def test_calculate_payload_passenger_count_non_integer(valid_flight):
    valid_flight.aircraft_data["Passengers"]["MAX"] = "not_a_integer"
    with pytest.raises(ValueError, match="Invalid passenger count data."):
        valid_flight.calculate_payload()


def test_calculate_payload_missing_passenger_data(valid_flight):
    del valid_flight.aircraft_data["Passengers"]

    with pytest.raises(
        ValueError, match="Passenger data for aircraft is missing."
    ):
        valid_flight.calculate_payload()


def test_calculate_cargo(valid_flight):
    expected_cargo = valid_flight.payload * 3.5 / 14
    cargo = valid_flight.calculate_cargo()
    assert cargo == expected_cargo


def test_calculate_zfw(valid_flight):
    expected_zfw = valid_flight.empty_weight + valid_flight.payload
    zfw = valid_flight.calculate_zfw()
    assert zfw == expected_zfw


def test_calculate_zfw_negative_integer(valid_flight):
    valid_flight.aircraft_data["ZWF"]["EMP"] = -1
    valid_flight.aircraft_data["ZWF"]["MAX"] = -1
    with pytest.raises(ValueError, match="Invalid count data."):
        valid_flight.calculate_zfw()


def test_calculate_zfw_non_integer(valid_flight):
    valid_flight.aircraft_data["ZWF"]["EMP"] = "not_a_integer"
    valid_flight.aircraft_data["ZWF"]["MAX"] = "not_a_integer"
    with pytest.raises(ValueError, match="Invalid count data."):
        valid_flight.calculate_zfw()


def test_calculate_zfw_missing_data(valid_flight):
    del valid_flight.aircraft_data["ZWF"]
    with pytest.raises(ValueError, match="ZFW data for aircraft is missing."):
        valid_flight.calculate_zfw()


def test_calculate_zfw_exceeding_max(valid_flight):
    valid_flight.aircraft_data["ZWF"]["MAX"] = (
        valid_flight.empty_weight + valid_flight.payload - 1
    )
    with pytest.raises(
        ValueError, match="Estimated ZFW exceeds maximum allowable ZFW."
    ):
        valid_flight.calculate_zfw()


def test_calculate_tow(valid_flight):
    expected_tow = (
        valid_flight.empty_weight
        + valid_flight.block_fuel
        + valid_flight.payload
    )
    tow = valid_flight.calculate_tow()
    assert tow == int(expected_tow)


def test_calculate_tow_negative_integer(valid_flight):
    valid_flight.aircraft_data["TOW"]["MAX"] = -1
    with pytest.raises(ValueError, match="Invalid count data."):
        valid_flight.calculate_tow()


def test_calculate_tow_non_integer(valid_flight):
    valid_flight.aircraft_data["TOW"]["MAX"] = "not_a_integer"
    with pytest.raises(ValueError, match="Invalid count data."):
        valid_flight.calculate_tow()


def test_calculate_tow_missing_data(valid_flight):
    del valid_flight.aircraft_data["TOW"]
    with pytest.raises(ValueError, match="TOW data for aircraft is missing."):
        valid_flight.calculate_tow()


def test_calculate_tow_exceeding_max(valid_flight):
    estimated_tow = int(
        valid_flight.empty_weight
        + valid_flight.block_fuel
        + valid_flight.payload
    )
    valid_flight.aircraft_data["TOW"]["MAX"] = estimated_tow - 1
    with pytest.raises(
        ValueError, match="Estimated TOW exceeds maximum allowable TOW."
    ):
        valid_flight.calculate_tow()


def test_calculate_lw(valid_flight):
    expected_lw = (
        valid_flight.estimated_tow
        - valid_flight.block_fuel
        + valid_flight.cargo
    )
    lw = valid_flight.calculate_lw()
    assert lw == int(expected_lw)


def test_calculate_lw_negative_integer(valid_flight):
    valid_flight.aircraft_data["LW"]["MAX"] = -1
    with pytest.raises(ValueError, match="Invalid count data."):
        valid_flight.calculate_lw()


def test_calculate_lw_non_integer(valid_flight):
    valid_flight.aircraft_data["LW"]["MAX"] = "not_a_integer"
    with pytest.raises(ValueError, match="Invalid count data."):
        valid_flight.calculate_lw()


def test_calculate_lw_missing_data(valid_flight):
    del valid_flight.aircraft_data["LW"]
    with pytest.raises(ValueError, match="LW data for aircraft is missing."):
        valid_flight.calculate_lw()


def test_calculate_lw_exceeding_max(valid_flight):
    estimated_lw = int(
        valid_flight.estimated_tow
        - valid_flight.block_fuel
        + valid_flight.cargo
    )
    valid_flight.aircraft_data["LW"]["MAX"] = estimated_lw - 1
    with pytest.raises(
        ValueError, match="Estimated LW exceeds maximum allowable LW."
    ):
        valid_flight.calculate_lw()
