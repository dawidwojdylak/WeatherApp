import pytest
from WeatherApp.WeatherFetcher import WeatherFetcher
from unittest import mock

class TestWeatherFetcher:
    CITY_NAME = 'Krakow'
    @pytest.mark.asyncio
    async def get_weather_fetcher_instance(self, callback = mock.MagicMock()):
        fetcher = WeatherFetcher(callback, self.CITY_NAME)
        await fetcher.setup()
        return fetcher

    @pytest.mark.asyncio
    async def test_get_city_coordinates(self):
        fetcher = await self.get_weather_fetcher_instance()
        lat, lon = await fetcher.get_city_coordinates()

        assert isinstance(lat, float)
        assert isinstance(lon, float)
        assert lat == 50.06143
        assert lon == 19.93658

    @pytest.mark.asyncio
    async def test_get_weather_data(self):
        async def callback(weather_data, units, city_name):
            assert city_name == self.CITY_NAME
            assert 'time' in units.keys()
            assert 'time' in weather_data.keys()
            assert 'rain' in units.keys()
            assert 'rain' in weather_data.keys()
            assert 'mm' in units.values()
        fetcher = await self.get_weather_fetcher_instance(callback=callback)
        await fetcher.get_weather_data()
