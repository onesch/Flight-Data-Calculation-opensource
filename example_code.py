from src.models.flight import Flight

flight = Flight(
    dep_icao="ulli",
    arr_icao="uuee",
    aircraft_icao="b738"
)

flight.print_flight_params()
# flight.save_to_json()
