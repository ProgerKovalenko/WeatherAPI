import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def get_weather(city:str):

    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    params = {
        'unitGroup': 'metric',
        'key': api_key,
        'contentType': 'json'
    }

    try:
        response = requests.get(f'{base_url}{city}', params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

if __name__ == "__main__":
    city_name = input("Enter city name: ")
    weather_data = get_weather(city_name)

    if weather_data:
        currentWeather = weather_data["currentConditions"]
        print(f"\nWeather in {weather_data['address']}:")
        print(f"Temperature: {currentWeather['temp']}C")
        print(f"Humidity: {currentWeather['humidity']}%")
        print(f"Condition: {currentWeather['conditions']}")