import os
import requests


WEATHER_API_KEY = os.environ['WEATHER_API_KEY']


def _get_weather_api():
    return requests.get(f'http://api.openweathermap.org/data/2.5/weather?id=4509177&appid={WEATHER_API_KEY}')


def get_weather():
    response = _get_weather_api()
    return response.json()['weather'][0]['main'].lower()


def get_temperature():
    response = _get_weather_api()
    return f"{(response.json()['main']['temp'] * (9 / 5) - 459.67):.0f} °F"


def get_humidity():
    response = _get_weather_api()
    return response.json()['main']['humidity']
