import json
import requests
import asyncio

class WeatherFetcher:
    # status code 200 means that the request was successful
    SUCCESSFUL_REQUEST = 200
    BASE_OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, callback, location_data):
        self.callback = callback
        self.API = self.BASE_OPEN_METEO_API_URL + f"?latitude={location_data.get("latitude")}&longitude={location_data.get("longitude")}&hourly=temperature_2m,rain"

        self.city_name = location_data.get("name")

    def get_city_name(self):
        return self.city_name

    async def get_weather_data(self):
        while True:
            await asyncio.sleep(1) # TODO: remove sleep
            response = requests.get(self.API)
            if response.status_code == self.SUCCESSFUL_REQUEST:
                data = response.json()
                units = data.get('hourly_units')
                weather_data = data.get('hourly')
                await self.callback(weather_data, units)
            break
