from send_message import send_message
from weather import get_weather


def send_sky_piss():
    weather = get_weather()

    if 'rain' in weather or 'storm' in weather:
        send_message('the sky is full of piss')


if __name__ == '__main__':
    send_sky_piss()
