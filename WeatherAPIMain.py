import os
import redis
import requests
from dotenv import load_dotenv
import json

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


def set_up_redis() -> redis.Redis:
    r = redis.Redis(host='localhost', port=6379)
    return r


def get_user_city() -> str:
    user_city =input(str("Enter City: "))
    return user_city

def check_city_in_cache(r:redis.Redis, city:str):
    cached_city = r.get(city)

    if cached_city is not None:
        print(f"Cache for {city} is cached")
        cache_weather_data = json.loads(cached_city)
        print_weather_data(cache_weather_data)
    else:
        print(f"Cache for {city} is not cached")
        weather_data = get_weather(city)
        json_weather_data = json.dumps(weather_data, indent=4,ensure_ascii=False)
        r.set(city, json_weather_data)
        print_weather_data(weather_data)


def print_weather_data(weather_data:dict):
    current_weather = weather_data["currentConditions"]
    print(f"\nWeather in {weather_data['address']}:")
    print(f"Temperature: {current_weather['temp']}C")
    print(f"Humidity: {current_weather['humidity']}%")
    print(f"Condition: {current_weather['conditions']}")


if __name__ == "__main__":
    while True:
        check_city_in_cache(set_up_redis(), get_user_city())