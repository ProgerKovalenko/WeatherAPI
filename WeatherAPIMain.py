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
        if response.status_code == 400:
            print(f"City {city} is not available")
            return None
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as exception:
        print(f"Connection error: {exception}")
        return None


def set_up_redis() -> redis.Redis:
    r = redis.Redis(host='localhost', port=6379)
    return r


def get_user_city() -> str:
    city =input(str("Enter City: "))
    return city


def check_city_in_cache(r:redis.Redis, city:str):
    try:
        cached_city = r.get(city)

    except redis.exceptions.ConnectionError:
        print('Warning:Redis connection error. Working without cache')
        cached_city = None

    if cached_city is not None:
        print(f"Cache for {city} is cached")
        cache_weather_data = json.loads(cached_city)
        print_weather_data(cache_weather_data)
    else:
        print(f"Cache for {city} is not cached")
        weather_data = get_weather(city)
        if weather_data:
            print_weather_data(weather_data)
            try:
                json_weather_data = json.dumps(weather_data, indent=4,ensure_ascii=False)
                r.set(city, json_weather_data, ex = 43200)
            except redis.exceptions.ConnectionError:
                pass
        else:
            print('Could not find any weather data for this city')


def print_weather_data(weather_data:dict):
    current_weather = weather_data["currentConditions"]
    print(f"\nWeather in {weather_data['address']}:")
    print(f"Temperature: {current_weather['temp']}C")
    print(f"Humidity: {current_weather['humidity']}%")
    print(f"Condition: {current_weather['conditions']}")


if __name__ == "__main__":
    r_client = set_up_redis()
    while True:
        user_city = get_user_city()
        if user_city.lower() == 'exit' : break
        check_city_in_cache(r_client,user_city)