from send_message import send_message
import json
import requests
from PIL import Image
from io import BytesIO
from datetime import date
import secrets
import groupme_image_service


def send_alex():

    # get days since this joke started
    days_since_start = (date.today() - date(2020, 12, 4)).days
    message_text = f'day {days_since_start} of rotating alex gonzalez 1 degree per day until h-row goes down the ramp on game day'

    # rotate image
    with BytesIO() as output:
        with Image.open(secrets.PATH_TO_ALEX) as img:
            rotate_img= img.rotate(-days_since_start)
            rotate_img.save(output, 'jpeg')
        data = output.getvalue()

    # run image through GroupMe image service
    image_url = groupme_image_service.upload_image_data(data)

    # send message
    send_message(message_text, image_url)


if __name__ == '__main__':
    send_alex()
