from math import radians, sin, cos, sqrt, atan2
from src.models.airport import Airport
from src.models.aircraft import Aircraft
import json
from typing import Any


class Flight:
    """
    Represents a flight from a departure airport to
    an arrival airport using a specific aircraft.
    The class calculates various flight parameters based on the
    provided ICAO codes of the departure and arrival airports,
    as well as the aircraft. These parameters include distance,
    block fuel, payload, and weights (ZFW, TOW, and LW).

    Args:
        dep_icao (str): ICAO code of the departure airport.
        arr_icao (str): ICAO code of the arrival airport.
        aircraft_icao (str): ICAO code of the
            aircraft being used for the flight.
    """

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
        self.empty_weight: int = 0
        self.estimated_zfw: int = 0
        self.max_zfw: int = 0
        self.estimated_tow: int = 0
        self.max_tow: int = 0
        self.estimated_lw: int = 0
        self.max_lw: int = 0
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

    def _to_dict(self) -> dict[str, Any]:
        """Returns flight calculations as a dictionary."""
        return {
            "aircraft": self.aircraft.aircraft_icao,
            "departure": {
                "icao": self.dep_airport.icao_code,
                "latitude": self.dep_airport.latitude,
                "longitude": self.dep_airport.longitude,
            },
            "arrival": {
                "icao": self.arr_airport.icao_code,
                "latitude": self.arr_airport.latitude,
                "longitude": self.arr_airport.longitude,
            },
            "parameters": {
                "distance_km": int(self.distance_km),
                "passengers_max": self.passengers_count,
                "block_fuel_kg": int(self.block_fuel),
                "payload_kg": int(self.payload),
                "cargo_kg": int(self.cargo),
                "zfw": {
                    "est": int(self.estimated_zfw),
                    "max": int(self.max_zfw)
                },
                "tow": {
                    "est": int(self.estimated_tow),
                    "max": int(self.max_tow)
                },
                "lw": {
                    "est": int(self.estimated_lw),
                    "max": int(self.max_lw)
                },
            },
        }

    def save_to_json(self) -> None:
        """Saves flight calculations to a JSON file."""
        filename = (
            f"route-{self.aircraft.aircraft_icao}"
            + f"-{self.dep_airport.icao_code}-"
            + f"to-{self.arr_airport.icao_code}.json"
        )
        try:
            with open(filename, "w") as file:
                json.dump(self._to_dict(), file, indent=4)
        except IOError as e:
            raise IOError(f"Error saving JSON file: {e}")

    def print_flight_params(self) -> None:
        """Prints the flight parameters."""
        print(
            f"\nAircraft: {self.aircraft.aircraft_icao}",
            f"\n{self.dep_airport.icao_code}"
            + f" lat:{self.dep_airport.latitude},"
            + f" lon:{self.dep_airport.longitude}",
            f"\n{self.arr_airport.icao_code}"
            + f" lat:{self.arr_airport.latitude},"
            + f" lon:{self.arr_airport.longitude}",
            f"\nDistance: {self.distance_km:.0f} km\n",
            f"\nPassengers [max]: {self.passengers_count}",
            f"\nBlock Fuel: {self.block_fuel:.0f} kg",
            f"\nPayload: {self.payload} kg",
            f"\nCargo: {self.cargo:.0f} kg\n",
            f"\nZFW est:{self.estimated_zfw}, max:{self.max_zfw}",
            f"\nTOW est:{self.estimated_tow}, max:{self.max_tow}",
            f"\nLW est:{self.estimated_lw}, max:{self.max_lw}\n",
        )

    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculates the distance between
        two points using the Haversine formula.
        """
        if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
            raise ValueError(
                "Latitude must be between -90 and 90 degrees."
            )
        if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
            raise ValueError(
                "Longitude must be between -180 and 180 degrees."
            )

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
        base_coefficient = 1.5
        additional_coefficient = (self.distance_km // 100) * 0.3
        total_coefficient = base_coefficient + additional_coefficient

        if total_coefficient == 0:
            raise ValueError("Total coefficient cannot be zero.")

        return self.distance_km / 100 / total_coefficient

    def calculate_block_fuel(self) -> float:
        """
        Calculates the block fuel required for the flight.
        """
        try:
            fuel_on_100km = int(self.aircraft_data["FuelOn100km"]["MAX"])
            distance_100km = self._distance_100km()
            block_fuel = fuel_on_100km * distance_100km
            return block_fuel

        except ZeroDivisionError:
            raise ValueError("Distance calculation resulted in zero.")
        except KeyError:
            raise ValueError("Fuel data for aircraft is missing.")

    def calculate_distance_km(self) -> float:
        """
        Calculates the distance between two airports.
        """
        try:
            distance_km = self._haversine_distance(
                self.dep_airport.latitude,
                self.dep_airport.longitude,
                self.arr_airport.latitude,
                self.arr_airport.longitude,
            )
            return distance_km

        except TypeError:
            raise ValueError(
                "Invalid coordinates for departure or arrival airports."
            )

    def calculate_payload(self) -> int:
        """
        Calculates the total payload on
        board based on the number of passengers.
        """
        try:
            self.passengers_count = self.aircraft_data["Passengers"]["MAX"]
            if not isinstance(
                self.passengers_count, int
            ) or self.passengers_count < 0:
                raise ValueError("Invalid passenger count data.")
            passenger = 104
            payload = self.passengers_count * passenger
            return payload

        except KeyError:
            raise ValueError("Passenger data for aircraft is missing.")

    def calculate_cargo(self) -> float:
        """
        Calculates the total cargo weight
        on board based on the number of passengers.
        """
        try:
            cargo_per_passenger = 3.5
            cargo = self.payload * cargo_per_passenger / 14
            return cargo

        except ZeroDivisionError:
            raise ValueError(
                "Cargo calculation encountered division by zero."
            )

    def calculate_zfw(self) -> int:
        """
        Calculates the estimated Zero Fuel Weight (ZFW).

        ZFW is the total weight of the aircraft without any fuel on board.
        It is calculated as the sum of the empty weight and the payload.

        Returns:
            int: Estimated ZFW in kilograms.
        """
        try:
            self.empty_weight = self.aircraft_data["ZWF"]["EMP"]
            self.max_zfw = self.aircraft_data["ZWF"]["MAX"]

            if (
                not isinstance(self.empty_weight, int)
                or not isinstance(self.max_zfw, int)
                or self.empty_weight < 0
                or self.max_zfw < 0
            ):
                raise ValueError("Invalid count data.")

            estimated_zfw = self.payload + self.empty_weight
            if estimated_zfw > self.max_zfw:
                raise ValueError(
                    "Estimated ZFW exceeds maximum allowable ZFW."
                )

            return estimated_zfw

        except KeyError:
            raise ValueError("ZFW data for aircraft is missing.")

    def calculate_tow(self) -> int:
        """
        Calculates the estimated Takeoff Weight (TOW).

        TOW is the total weight of the aircraft at the time of takeoff.
        It includes the empty weight, block fuel, and payload.

        Returns:
            int: Estimated TOW in kilograms.
        """
        try:
            self.max_tow = self.aircraft_data["TOW"]["MAX"]
            if not isinstance(self.max_tow, int) or self.max_tow < 0:
                raise ValueError("Invalid count data.")

            estimated_tow = self.empty_weight + self.block_fuel + self.payload
            estimated_tow = int(estimated_tow)

            if estimated_tow > self.max_tow:
                raise ValueError(
                    "Estimated TOW exceeds maximum allowable TOW."
                )

            return estimated_tow

        except KeyError:
            raise ValueError("TOW data for aircraft is missing.")

    def calculate_lw(self) -> int:
        """
        Calculates the estimated Landing Weight (LW).

        LW is the total weight of the aircraft upon landing.
        It is calculated as the estimated TOW minus the block fuel
        and includes the cargo weight.

        Returns:
            int: Estimated LW in kilograms.
        """
        try:
            self.max_lw = self.aircraft_data["LW"]["MAX"]
            if not isinstance(self.max_lw, int) or self.max_lw < 0:
                raise ValueError("Invalid count data.")

            estimated_lw = self.estimated_tow - self.block_fuel + self.cargo
            estimated_lw = int(estimated_lw)

            if estimated_lw > self.max_lw:
                raise ValueError(
                    "Estimated LW exceeds maximum allowable LW."
                )
            return estimated_lw

        except KeyError:
            raise ValueError("LW data for aircraft is missing.")
