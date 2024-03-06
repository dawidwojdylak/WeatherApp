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

    args = parser.parse_args()
    return args

def read_config_file():
    config_p = configparser.ConfigParser()
    try:
        with open("config.ini", "r") as f:
            config_p.read_file(f)

    except FileNotFoundError:
        config_p.add_section("location")
        config_p.set("location", "latitude", "51.10")
        config_p.set("location", "longitude", "17.03")
        config_p.set("location", "name", "Wroclaw")
        config_p.set("location", "any_condition_met", "True")

        with open("config.ini", "w") as config_file:
            config_p.write(config_file)

    return dict(config_p["location"])


async def main():
    args = parse()
    config_file_data = read_config_file()
    processor = WeatherProcessor(args.temperature, args.rainfall,
        "True" == config_file_data.get("any_condition_met"))
    async def callback(weather_data, units):
        await processor.process_data(weather_data, units)
    fetcher = WeatherFetcher(callback, config_file_data)
    processor.set_city_name(fetcher.get_city_name())

    await fetcher.get_weather_data()


if __name__ == "__main__":
    asyncio.run(main())