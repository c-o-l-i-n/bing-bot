import bing_bot as bb
from weather import get_weather

def sky_piss():
    weather = get_weather()

    if 'rain' in weather or 'storm' in weather:
        bb.send_message('the sky is full of piss')

if __name__ == '__main__':
    sky_piss()
