import json
import os
from src.aircraft_data.manufacturers.manufacturers import manufacturers


class Aircraft:
    """
    Represents an aircraft with its associated data.

    This class is responsible for initializing an
    Aircraft object using its ICAO code.
    It loads relevant data about the aircraft, such as
    weight and fuel consumption,
    from a specified JSON file based on the manufacturer's code.
    """

    def __init__(self, aircraft_icao: str) -> None:
        """
        Initializes an Aircraft object with data about the aircraft.
        """
        if not aircraft_icao:
            raise ValueError("ICAO code cannot be empty.")
        self.aircraft_icao = aircraft_icao
        self.data = self.load_data()

    def load_data(self):
        """
        Loads data about the aircraft.
        """
        first_char = self.aircraft_icao[0].lower()
        manufacturer = manufacturers.get(first_char, None)

        if manufacturer:
            model = self.aircraft_icao.lower()
            file_path = (
                "src/aircraft_data/json_data/"
                + f"{manufacturer}/{model}/__init__.json"
            )

            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    return json.load(file)
            else:
                raise ValueError(
                    f"No data found for aircraft ICAO: {self.aircraft_icao}"
                )
        else:
            raise ValueError(
                f"Manufacturer not found for aircraft: {self.aircraft_icao}"
            )
