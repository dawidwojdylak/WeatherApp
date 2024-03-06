import json
import requests
import asyncio

class WeatherFetcher:
    # status code 200 means that the request was successful
    SUCCESSFUL_REQUEST = 200
    BASE_OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
    BASE_OPEN_METEO_GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, callback, city_name):
        self.callback = callback
            
        self.geocoding_api = self.BASE_OPEN_METEO_GEOCODING_API_URL \
            + f"?name={city_name}&count={1}&language=en&format=json"
        
        lat, lon = self.get_city_coordinates()

        self.meteo_api = self.BASE_OPEN_METEO_API_URL \
                        + f"?latitude={lat}" \
                        f"&longitude={lon}" \
                        f"&hourly=temperature_2m,rain"

    def get_city_coordinates(self):
        response = requests.get(self.geocoding_api)
        print(self.geocoding_api)
        if response.status_code == self.SUCCESSFUL_REQUEST:
            data = response.json()
            results = data.get('results')[0] # first result only
            self.city_name = results.get("name")
            return results.get("latitude"), results.get("longitude")

    async def get_weather_data(self):
        while True:
            await asyncio.sleep(1) # TODO: remove sleep
            response = requests.get(self.meteo_api)
            if response.status_code == self.SUCCESSFUL_REQUEST:
                data = response.json()
                units = data.get("hourly_units")
                weather_data = data.get("hourly")
                await self.callback(weather_data, units, self.city_name)
            break
