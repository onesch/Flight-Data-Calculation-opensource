import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CheckWXClient:
    BASE_URL = "https://api.checkwx.com"

    def __init__(self):
        self.api_key = os.getenv("CHECK_WX_API")
        if not self.api_key:
            raise EnvironmentError(
                "CHECK_WX_API key is missing in the environment."
            )

    def get_metar(self, icao: str) -> dict:
        """
        Retrieves METAR data for a given ICAO code from the CheckWX API.

        :param icao: The ICAO code of the airport
        :return: Parsed JSON response from the API
        """
        url = f"{self.BASE_URL}/metar/{icao}/decoded"
        response = requests.get(url, headers={"X-API-Key": self.api_key})

        if response.status_code == 200:
            return response.json()
        raise ValueError(
            f"Error retrieving data for {icao}:"
            + f"{response.status_code} - {response.text}"
        )
