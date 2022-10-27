import logging
from send_message import send_message
from weather import get_humidity

def send_air_piss() -> None:
    humidity = get_humidity()
    threshold = 99

    if humidity >= threshold:
        send_message('the air is full of piss')
    else:
        logging.info(f'Humidity is not at or above {threshold}%; no message sent.')
    

if __name__ == '__main__':
    send_air_piss()
