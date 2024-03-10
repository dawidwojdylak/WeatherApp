## Weather Alert Application

This Python script provides weather alerts based on user defined thresholds for temperature and rainfall. It uses the Open-Meteo API to fetch weather data for a specified city.

### Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required [aiohttp](https://docs.aiohttp.org/en/stable/) package.

```bash
pip install aiohttp
```

### Usage

```
usage: main.py [-h] -t TEMPERATURE -r RAINFALL [-c CITYNAME] [-i]
```

### Options

- `-h`, `--help`: Show help message and exit.
- `-t TEMPERATURE`, `--temperature TEMPERATURE`: Set the temperature bottom threshold in Celcius degrees.
- `-r RAINFALL`, `--rainfall RAINFALL`: Set the rainfall top threshold in milimeters.
- `-c CITYNAME`, `--cityname CITYNAME`: Specify the name of the city for which weather alerts will be generated. Default is set to a predefined city.
- `-i`, `--independent`: If this option is used, the weather log will be displayed if either of the thresholds is exceeded. If not, both the temperature and rain thresholds must be exceeded.

### Example

```
user@ThinkPad:~/WeatherApp$ python ./main.py -t 10 -r .1 Krakow
-------------------------REPORT for Krakow-------------------------
Warning Krakow, low temperature 9.5 of °C and rain 0.1 mm expected on 2024-03-10T20:00
Warning Krakow, low temperature 8.4 of °C and rain 0.1 mm expected on 2024-03-11T02:00
Warning Krakow, low temperature 8.4 of °C and rain 0.1 mm expected on 2024-03-11T03:00
Warning Krakow, low temperature 8.5 of °C and rain 0.1 mm expected on 2024-03-11T04:00
Warning Krakow, low temperature 8.4 of °C and rain 0.2 mm expected on 2024-03-11T05:00
```

### Tests
To run the unit tests, also install
```bash
pip install pytest pytest-asyncio
```
and run
```bash
pytest tests/TestWeatherFetcher.py
```
