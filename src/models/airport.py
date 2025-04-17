# airport.py


class Airport:
    def __init__(self, icao: str, api_client) -> None:
        """
        Initializes an Airport object and
        retrieves data using the provided API client.

        :param icao: The ICAO code of the airport
        :param api_client: An instance of a client
        that implements get_metar(icao)
        """
        self.icao: str = icao
        self.icao_code: str = "Unknown"
        self.latitude: float = 0.0
        self.longitude: float = 0.0
        self.api_client = api_client
        self.get_data()

    def get_data(self):
        """
        Fetches airport data using the provided API client
        and populates the attributes.
        """
        data = self.api_client.get_metar(self.icao)
        if "data" in data and len(data["data"]) > 0:
            airport_data = data["data"][0]
            self.icao_code = airport_data.get("icao", "Unknown")
            coords = airport_data["station"]["geometry"]["coordinates"]
            self.longitude, self.latitude = coords
        else:
            raise ValueError(
                f"The airport with ICAO code {self.icao} does not exist."
            )
