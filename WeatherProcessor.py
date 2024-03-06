class WeatherProcessor:
    def __init__(self, low_temp_limit, high_rain_limit):
        self.low_temp_limit = low_temp_limit
        self.high_rain_limit = high_rain_limit
        self.city_name = None

    async def process_data(self, weatherData, units):
        low_temp_indices = [idx for idx, val in enumerate(weatherData.get("temperature_2m", [])) if val <= self.low_temp_limit]
        high_rain_indices = [idx for idx, val in enumerate(weatherData.get("rain", [])) if val >= self.high_rain_limit]

        indices = sorted(list(set(low_temp_indices + high_rain_indices)))
        # indices = set(low_temp_indices + high_rain_indices)

        text_fill = 25 * '-'
        text = f"{text_fill}REPORT{text_fill}"
        for i in indices:
            text += f"Warning {self.city_name}, "
            temp_flag = False

            if i in low_temp_indices:
                text += f"low temperature {weatherData.get("temperature_2m")[i]} of {units.get("temperature_2m")} "
                temp_flag = True

            if i in high_rain_indices:
                if temp_flag: text += "and "
                text += f"rain {weatherData.get("rain")[i]} {units["rain"]} "

            text += f"expected on {weatherData.get("time")[i]}\n"

        print(text)

    def set_city_name(self, name):
        self.city_name = name
