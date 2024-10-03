import requests
import os
from dotenv import load_dotenv


load_dotenv()
API = os.getenv("CHECK_WX_API")


class Airport:
    BASE_URL = "https://api.checkwx.com/metar/"

    def __init__(self, icao: str) -> None:
        """
        Initializes an Airport object and
        retrieves data for the specified ICAO code.

        :param icao: The ICAO code of the airport
        """
        self.icao: str = icao
        self.icao_code: str = "Unknown"
        self.latitude: float = 0.0
        self.longitude: float = 0.0
        self.get_data()

    def get_data(self):
        """
        Fetches airport data from the CheckWX API and
        populates the airport attributes.
        Raises an exception if the airport does not exist or
        if the request fails.
        """
        url = f"{self.BASE_URL}{self.icao}/decoded"
        res = requests.get(url, headers={"X-API-Key": API})

        if res.status_code == 200:
            data = res.json()
            if "data" in data and len(data["data"]) > 0:
                self.icao_code = data["data"][0].get("icao", "Unknown")
                coords: list[float] = data["data"][0]["station"]["geometry"][
                    "coordinates"
                ]
                self.longitude, self.latitude = coords[0], coords[1]  # !
            else:
                raise ValueError(
                    f"The airport with ICAO code {self.icao} does not exist."
                )
        else:
            raise ValueError(
                f"Error retrieving data for {self.icao}: {
                    res.status_code
                } - {res.text}"
            )
