import requests


def get_coordinates(location):
    """
    Converts a city or town name into latitude and longitude.
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            return None

        result = data["results"][0]

        return {
            "name": result["name"],
            "country": result.get("country", ""),
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }

    except requests.exceptions.RequestException:
        return None


def get_wind_direction_text(degrees):
    """
    Converts wind direction degrees into compass direction.
    """

    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]

    index = round(degrees / 22.5) % 16
    return directions[index]


def get_weather_code_description(code):
    """
    Converts Open-Meteo weather code into a readable condition.
    """

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    return weather_codes.get(code, "Unknown conditions")


def get_weather_data(location):
    """
    Gets detailed current weather data for a location.
    This is used by the Streamlit GUI.
    """

    coordinates = get_coordinates(location)

    if coordinates is None:
        return {
            "success": False,
            "error": f"Sorry, I could not find the location '{location}'. Please try another city."
        }

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "precipitation,"
            "rain,"
            "weather_code,"
            "cloud_cover,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "wind_gusts_10m"
        ),
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data.get("current")

        if not current:
            return {
                "success": False,
                "error": "Sorry, I could not get the current weather right now."
            }

        wind_direction_degrees = current.get("wind_direction_10m", 0)

        return {
            "success": True,
            "location": coordinates["name"],
            "country": coordinates["country"],
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "precipitation": current.get("precipitation"),
            "rain": current.get("rain"),
            "weather_code": current.get("weather_code"),
            "condition": get_weather_code_description(current.get("weather_code")),
            "cloud_cover": current.get("cloud_cover"),
            "wind_speed": current.get("wind_speed_10m"),
            "wind_direction_degrees": wind_direction_degrees,
            "wind_direction_text": get_wind_direction_text(wind_direction_degrees),
            "wind_gusts": current.get("wind_gusts_10m"),
            "is_day": "Day" if current.get("is_day") == 1 else "Night"
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Sorry, the weather service timed out. Please try again later."
        }

    except requests.exceptions.RequestException:
        return {
            "success": False,
            "error": "Sorry, there was a problem connecting to the weather API."
        }


def get_weather(location):
    """
    Gets current weather for a location.
    This keeps the terminal chatbot working.
    """

    weather = get_weather_data(location)

    if not weather["success"]:
        return weather["error"]

    return (
        f"Weather in {weather['location']}, {weather['country']}:\n"
        f"Condition: {weather['condition']}\n"
        f"Temperature: {weather['temperature']}°C\n"
        f"Feels like: {weather['feels_like']}°C\n"
        f"Humidity: {weather['humidity']}%\n"
        f"Cloud cover: {weather['cloud_cover']}%\n"
        f"Rain: {weather['rain']} mm\n"
        f"Wind speed: {weather['wind_speed']} km/h\n"
        f"Wind gusts: {weather['wind_gusts']} km/h\n"
        f"Wind direction: {weather['wind_direction_degrees']}° {weather['wind_direction_text']}"
    )