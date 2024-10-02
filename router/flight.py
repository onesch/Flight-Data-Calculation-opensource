from math import radians, sin, cos, sqrt, atan2
from router.airport import Airport
from router.aircraft import Aircraft


class Flight:
    def __init__(self, dep_icao: str, arr_icao: str, aircraft_icao: str):
        self.aircraft = Aircraft(aircraft_icao)
        self.aircraft_data = self.aircraft.data[self.aircraft.aircraft_icao]
        self.dep_airport = Airport(dep_icao)
        self.arr_airport = Airport(arr_icao)
        self.distance_km: float = 0.0
        self.block_fuel: float = 0.0
        self.payload: int = 0
        self.cargo: float = 0.0
        self.passengers_count: int = 0
        self.empty_weight: float = 0.0
        self.estimated_zfw: float = 0.0
        self.max_zfw: float = 0.0
        self.estimated_tow: float = 0.0
        self.max_tow: float = 0.0
        self.estimated_lw: float = 0.0
        self.max_lw: float = 0.0
        self.calculate_flight_params()

    def calculate_flight_params(self) -> None:
        """Calculates the flight parameters."""
        self.distance_km = self.calculate_distance_km()
        self.block_fuel = self.calculate_block_fuel()
        self.payload = self.calculate_payload()
        self.cargo = self.calculate_cargo()
        self.estimated_zfw = self.calculate_zfw()
        self.estimated_tow = self.calculate_tow()
        self.estimated_lw = self.calculate_lw()
        self.print_flight_params()

    def print_flight_params(self) -> None:
        """Prints the flight parameters."""
        print(
            f"\nAircraft: {self.aircraft.aircraft_icao}",
            f"\n{self.dep_airport.icao_code} lat:{self.dep_airport.latitude}, lon:{self.dep_airport.longitude}",
            f"\n{self.arr_airport.icao_code} lat:{self.arr_airport.latitude}, lon:{self.arr_airport.longitude}",
            f"\nDistance: {self.distance_km:.0f} km\n",
            f"\nPassengers [max]: {self.passengers_count}",
            f"\nBlock Fuel: {self.block_fuel:.0f} kg",
            f"\nPayload: {self.payload} kg",
            f"\nCargo: {self.cargo:.0f} kg\n",
            f"\nZFW est:{self.estimated_zfw:.0f}, max:{self.max_zfw:.0f}",
            f"\nTOW est:{self.estimated_tow:.0f}, max:{self.max_tow:.0f}",
            f"\nLW est:{self.estimated_lw:.0f}, max:{self.max_lw:.0f}\n"
        )

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

        return block_fuel

    def calculate_distance_km(self) -> float:
        """
        Calculates the distance between two airports.
        """
        distance_km = self._haversine_distance(
            self.dep_airport.latitude,
            self.dep_airport.longitude,
            self.arr_airport.latitude,
            self.arr_airport.longitude,
        )

        return distance_km

    def calculate_payload(self) -> int:
        """
        Calculates the total payload on
        board based on the number of passengers.
        """
        self.passengers_count = int(self.aircraft_data["Passengers"]["MAX"])
        passenger = 104
        payload = self.passengers_count * passenger

        return payload

    def calculate_cargo(self) -> float:
        """
        Calculates the total cargo weight
        on board based on the number of passengers.
        """
        cargo_per_passenger = 3.5
        cargo = self.payload * cargo_per_passenger / 14

        return cargo

    def calculate_zfw(self) -> float:
        """
        Calculates the estimated Zero Fuel Weight (ZFW).

        ZFW is the total weight of the aircraft without any fuel on board. 
        It is calculated as the sum of the empty weight and the payload.

        Returns:
            float: Estimated ZFW in kilograms.
        """
        self.empty_weight = float(self.aircraft_data["ZWF"]["EMP"])
        self.max_zfw = float(self.aircraft_data["ZWF"]["MAX"])
        estimated_zfw = self.payload + self.empty_weight

        return estimated_zfw

    def calculate_tow(self) -> float:
        """
        Calculates the estimated Takeoff Weight (TOW).

        TOW is the total weight of the aircraft at the time of takeoff. 
        It includes the empty weight, block fuel, and payload.

        Returns:
            float: Estimated TOW in kilograms.
        """
        self.max_tow = float(self.aircraft_data["TOW"]["MAX"])
        estimated_tow = (
            self.empty_weight
            + self.block_fuel
            + self.payload
        )

        return estimated_tow

    def calculate_lw(self) -> float:
        """
        Calculates the estimated Landing Weight (LW).

        LW is the total weight of the aircraft upon landing. 
        It is calculated as the estimated TOW minus the block fuel
        and includes the cargo weight.

        Returns:
            float: Estimated LW in kilograms.
        """
        self.max_lw = float(self.aircraft_data["LW"]["MAX"])
        estimated_lw = self.estimated_tow - self.block_fuel + self.cargo

        return estimated_lw
