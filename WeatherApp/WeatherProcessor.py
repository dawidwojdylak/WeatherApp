class WeatherProcessor:
    def __init__(self, low_temp_limit, high_rain_limit,
                 independent):
        self.low_temp_limit = low_temp_limit
        self.high_rain_limit = high_rain_limit
        self.independent = independent

    async def process_data(self, weatherData, units, name):
        low_temp_indices = [
            idx for idx, val 
            in enumerate(weatherData.get("temperature_2m", []))
            if val <= self.low_temp_limit
            ]
        high_rain_indices = [
            idx for idx, val 
            in enumerate(weatherData.get("rain", []))
            if val >= self.high_rain_limit
            ]

        if self.independent:
            indices = sorted(list(set(low_temp_indices
                        + high_rain_indices)))
        else:
            indices = sorted(list(set(low_temp_indices)
                        & set(high_rain_indices)))

        text_fill = 25 * "-"
        text = f"{text_fill}REPORT for {name}{text_fill}\n"
        for i in indices:
            text += f"Warning {name}, "
            temp_flag = False

            if i in low_temp_indices:
                text += f"low temperature " \
                        f"{weatherData.get('temperature_2m')[i]} of " \
                        f"{units.get('temperature_2m')} "
                temp_flag = True

            if i in high_rain_indices:
                if temp_flag:
                    text += "and "
                text += f"rain {weatherData.get('rain')[i]} " \
                        f"{units['rain']} "

            text += f"expected on {weatherData.get('time')[i]}\n"

        print(text)
