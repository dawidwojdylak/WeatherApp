import asyncio
import aiohttp

class WeatherFetcher:
    """A class for fetching weather data."""
    # status code 200 means that the request was successful
    SUCCESSFUL_REQUEST = 200
    BASE_OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
    BASE_OPEN_METEO_GEOCODING_API_URL = \
        "https://geocoding-api.open-meteo.com/v1/search"
    def __init__(self, callback, city_name):
        """Initialize weather fetcher object.
        
        Args:
            callback (function): A callback for function which processes
                                the weather data. The function shall take
                                following arguments:
                                    weather_data (dict)
                                    units (dict)
                                    city_name
            city_name (str): Name of the desired city.
        """
        self.callback = callback
        self.city_name = city_name
        self.meteo_api = None
        self.geocoding_api = None

    async def setup(self):
        """Prepare API URLs. Must be called after 
        the constructor manually, because it needs to be awaited."""
        self.geocoding_api = f"{self.BASE_OPEN_METEO_GEOCODING_API_URL}" \
            f"?name={self.city_name}&count={1}&language=en&format=json"
        
        lat, lon = await self.get_city_coordinates()
        if lat is not None and lon is not None:
            self.meteo_api = f"{self.BASE_OPEN_METEO_API_URL}" \
                            f"?latitude={lat}" \
                            f"&longitude={lon}" \
                            f"&hourly=temperature_2m,rain"

    async def get_city_coordinates(self):
        """Get city coordinates.
        
        Returns:
            tuple: A tuple containing latitude and longitude.
        """
        lat = None
        lon = None
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.geocoding_api) as response:
                    data = await response.json()
                    if data:
                        results = data.get('results') 
                        if results:
                            results = results[0] # first result only
                            self.city_name = results.get("name") 
                            lat = results.get("latitude")
                            lon = results.get("longitude")
                        else:
                            print(f"Details for the city " \
                                  f"\"{self.city_name}\" were not found.")
            except aiohttp.ClientConnectionError as e:
                print(f"Connection error: {e}")
        return lat, lon

    async def get_weather_data(self):
        """Get city coordinates. 
        Pass the weather data to the callback function.
        """
        async with aiohttp.ClientSession() as session:
            try:
                if self.meteo_api:
                    async with session.get(self.meteo_api) as response:
                        data = await response.json()
                        units = data.get("hourly_units")
                        weather_data = data.get("hourly")
                        await self.callback(weather_data, units, 
                                            self.city_name)
                else:
                    print("Weather data is not available.")
            except aiohttp.ClientConnectionError as e:
                print(f"Connection error: {e}")
