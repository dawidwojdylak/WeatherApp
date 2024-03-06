import json
import requests
import asyncio

OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_API_URL_JSON = "https://api.open-meteo.com/v1/forecast?latitude=51.10&longitude=17.03&hourly=temperature_2m,rain"

class WeatherFetcher:
    # status code 200 means that the request was successful
    SUCCESSFUL_REQUEST = 200

    def __init__(self, callback):
        self.callback = callback

        self.weather_params = {
            "latitude": 51.10,
            "longitude": 17.03,
            "hourly": ["temperature_2m", "precipitation"],
            "current": ["temperature_2m", "precipitation"],
        }

        self.city_name = self.obtain_city_name()

    def obtain_city_name(self):
        # api_key = ''
        # latitude = "51.10"
        # longitude = "17.03"
        # # url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
        # url = f'https://geocoding-api.open-meteo.com/v1/search?latitude={latitude}&longitude={longitude}&count=1&language=en&format=json'
        # print(url)
        # try:
        #     response = requests.get(url)
        #     data = response.json()
        #     city_name = data['name']
        #     return city_name
        # except Exception as e:
        #     print("An error occured:", e)
        #     return None

        return "Wroclaw"
        
    def get_city_name(self):
        return self.city_name

    async def get_weather_data(self):
        while True:
            await asyncio.sleep(1)
            response = requests.get(OPEN_METEO_API_URL_JSON)
            if response.status_code == self.SUCCESSFUL_REQUEST:
                data = response.json()
                units = data.get('hourly_units')
                weather_data = data.get('hourly')
                await self.callback(weather_data, units)
            break
