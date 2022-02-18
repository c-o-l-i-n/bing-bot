from send_message import send_message
from weather import get_humidity

def send_air_piss():
    humidity = get_humidity()

    if humidity >= 95:
        send_message('the air is full of piss')

if __name__ == '__main__':
    send_air_piss()
