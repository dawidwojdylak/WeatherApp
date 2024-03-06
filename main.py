import argparse
import asyncio
from WeatherFetcher import WeatherFetcher
from WeatherProcessor import WeatherProcessor

def parse():
    parser = argparse.ArgumentParser()
    parser.description = "A script that prints weather alerts."
    parser.add_argument("-t", "--temperature", type=float, help="Temperature bottom threshold [Celc deg].", required=True)
    parser.add_argument("-r", "--rainfall", type=float, help="Rainfall top threshold [mm].", required=True)

    args = parser.parse_args()
    return args


async def main():
    args = parse()

    processor = WeatherProcessor(args.temperature, args.rainfall)
    async def callback(weather_data, units):
        await processor.process_data(weather_data, units)
    fetcher = WeatherFetcher(callback)
    processor.set_city_name(fetcher.get_city_name())

    await fetcher.get_weather_data()


if __name__ == "__main__":
    asyncio.run(main())