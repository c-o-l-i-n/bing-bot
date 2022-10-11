from http import HTTPStatus
import os
import logging
import requests
from dotenv import load_dotenv


load_dotenv()
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']


def _get_weather_data():
    logging.info('Getting current weather data for Columbus')
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id=4509177&appid={OPENWEATHER_API_KEY}')

    if response.status_code != HTTPStatus.OK:
        logging.error(response.text)
        response.raise_for_status() 

    logging.info(response.text)
    return response.json()


def get_weather():
    return _get_weather_data()['weather'][0]['main'].lower()


def get_temperature():
    return f"{(_get_weather_data()['main']['temp'] * (9 / 5) - 459.67):.0f} °F"


def get_humidity():
    return _get_weather_data()['main']['humidity']
