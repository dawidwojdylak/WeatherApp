import argparse
import asyncio
import configparser
from WeatherFetcher import WeatherFetcher
from WeatherProcessor import WeatherProcessor

def parse():
    parser = argparse.ArgumentParser()
    parser.description = "A script that prints weather alerts."
    parser.add_argument("-t", "--temperature", type=float,
                        help="Temperature bottom threshold [Celc deg].",
                        required=True)
    parser.add_argument("-r", "--rainfall", type=float,
                        help="Rainfall top threshold [mm].", required=True)
    
    parser.add_argument("-c", "--cityname", type=str, default="Wroclaw")
    parser.add_argument("-i", "--independent", action="store_true",
                        help="If this option is used, the weather " \
                            "log will be displayed if either of the " \
                            "thresholds is exceeded. If not, both " \
                            " the temperature and rain thresholds " \
                            "must be exceeded.")

    args = parser.parse_args()
    return args

async def main():
    args = parse()
    processor = WeatherProcessor(args.temperature, args.rainfall,
                                 args.independent)
    async def callback(weather_data, units, name):
        await processor.process_data(weather_data, units, name)
    fetcher = WeatherFetcher(callback, args.cityname)

    await fetcher.get_weather_data()

if __name__ == "__main__":
    asyncio.run(main())