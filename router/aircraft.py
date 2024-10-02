import json
import os

class Aircraft:
    def __init__(self, aircraft_icao: str) -> None:
        """
        Initializes an Aircraft object with data about the aircraft.
        """
        self.aircraft_icao = aircraft_icao
        self.data = self.load_data()

    def load_data(self):
        """
        Loads data about the aircraft.
        """
        manufacturers = {
            "b": "boeing",
            "a": "airbus",
        }

        first_char = self.aircraft_icao[0].lower()
        manufacturer = manufacturers.get(first_char, None)

        if manufacturer:
            model = self.aircraft_icao.lower()
            file_path = f"aircraft_data/{manufacturer}/{model}/__init__.json"

            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    return json.load(file)
            else:
                raise ValueError(f"No data found for aircraft ICAO: {self.aircraft_icao}")
        else:
            raise ValueError(f"Manufacturer not found for aircraft ICAO: {self.aircraft_icao}")
