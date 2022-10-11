from http import HTTPStatus
import os
import logging
import requests


OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']


def _get_weather_data():
    logging.info('Getting current weather data for Columbus')
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id=4509177&appid={OPENWEATHER_API_KEY}')

    if response.status_code != HTTPStatus.OK:
        logging.error(response.text)
        response.raise_for_status() 

    logging.info(response.text)
    return response


def get_weather():
    try:
        response = _get_weather_data()
        return response.json()['weather'][0]['main'].lower()
    except:
        return ''


def get_temperature():
    try:
        response = _get_weather_data()
        return f"{(response.json()['main']['temp'] * (9 / 5) - 459.67):.0f} °F"
    except:
        return ''


def get_humidity():
    try:
        response = _get_weather_data()
        return response.json()['main']['humidity']
    except:
        return ''
