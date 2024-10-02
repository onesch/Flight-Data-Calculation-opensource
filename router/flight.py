from math import radians, sin, cos, sqrt, atan2
from router.airport import Airport
from router.aircraft import Aircraft


class Flight:
    def __init__(self, dep_icao: str, arr_icao: str, aircraft_icao: str):
        self.aircraft = Aircraft(aircraft_icao)
        self.aircraft_data = self.aircraft.data[self.aircraft.aircraft_icao]
        self.airport1 = Airport(dep_icao)
        self.airport2 = Airport(arr_icao)
        self.distance_km: float = 0.0
        self.block_fuel: float = 0.0
        self.payload: int = 0
        self.cargo: float = 0.0
        self.calculate_flight_params()

    def calculate_flight_params(self) -> None:
        """Calculates the flight parameters."""
        self.distance_km = self.calculate_distance_km()
        self.block_fuel = self.calculate_block_fuel()
        self.payload = self.calculate_payload()
        self.cargo = self.calculate_cargo()

    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculates the distance between two points using the Haversine formula.
        """
        R = 6371.0
        (lat1_rad, lon1_rad, lat2_rad, lon2_rad) = map(
            radians, [lat1, lon1, lat2, lon2]
        )
        dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
        a = (
            sin(dlat / 2) ** 2
            + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def _distance_100km(self) -> float:
        """
        Calculates the distance normalized per 100 km.
        """
        # x1, y1 = 250, 1.5
        # x2, y2 = 1500, 7.5
        # slope = (y2 - y1) / (x2 - x1)
        # intercept = y1 - slope * x1
        # s = slope * self.distance_km + intercept
        # return self.distance_km / 100 / s
        base_coefficient = 1.5
        additional_coefficient = (self.distance_km // 100) * 0.3
        total_coefficient = base_coefficient + additional_coefficient
        return self.distance_km / 100 / total_coefficient

        # print(f"Original distance: {self.distance_km} km")
        # print(f"Normalized coefficient: {total_coefficient}")

    def calculate_block_fuel(self) -> float:
        """
        Calculates the block fuel required for the flight.
        """
        fuel_on_100km = int(self.aircraft_data["FuelOn100km"]["MAX"])
        distance_100km = self._distance_100km()
        block_fuel = fuel_on_100km * distance_100km

        print(f"Block_fuel: {block_fuel:.0f} kg\n")
        return block_fuel

    def calculate_distance_km(self) -> float:
        """
        Calculates the distance between two airports.
        """
        distance_km = self._haversine_distance(
            self.airport1.latitude,
            self.airport1.longitude,
            self.airport2.latitude,
            self.airport2.longitude,
        )
        print(f"Distance: {distance_km:.0f} km\n")
        return distance_km

    def calculate_payload(self) -> int:
        """
        Calculates the total payload on
        board based on the number of passengers.
        """
        passengers_count = int(self.aircraft_data["Passengers"]["MAX"])
        passenger = 104
        payload = passengers_count * passenger

        print(f"Payload: {payload} kg\n")
        return payload

    def calculate_cargo(self) -> float:
        """
        Calculates the total cargo weight
        on board based on the number of passengers.
        """
        cargo_per_passenger = 3.5
        cargo = self.payload * cargo_per_passenger / 14

        print(f"Cargo: {cargo:.0f} kg")
        return cargo
