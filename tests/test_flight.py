from src.models.flight import Flight


def test_calculate_distance_km():
    flight = Flight("ULLI", "UUEE", "b738")
    assert flight.distance_km > 0


def test_calculate_payload():
    flight = Flight("ULLI", "UUEE", "b738")
    assert flight.payload == flight.passengers_count * 104


def test_calculate_zfw():
    flight = Flight("ULLI", "UUEE", "b738")
    expected_zfw = flight.empty_weight + flight.payload
    assert flight.estimated_zfw == expected_zfw


def test_calculate_tow():
    flight = Flight("ULLI", "UUEE", "b738")
    expected_tow = flight.empty_weight + flight.block_fuel + flight.payload
    assert flight.estimated_tow == expected_tow


def test_calculate_lw():
    flight = Flight("ULLI", "UUEE", "b738")
    expected_lw = flight.estimated_tow - flight.block_fuel + flight.cargo
    assert flight.estimated_lw == expected_lw
