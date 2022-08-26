import os
from send_message import send_message
from PIL import Image
from io import BytesIO
from datetime import date
import groupme_image_service
from dotenv import load_dotenv


load_dotenv()
PATH_TO_ALEX = os.environ['PATH_TO_ALEX']


def send_alex_last():

    # get days since this joke started
    days_since_start = (date.today() - date(2020, 12, 4)).days
    message_text = f"this is it. today's the day. day {days_since_start} of rotating alex gonzalez 1 degree per day until h-row goes down the ramp in just a few short hours for the first time in 2 years. good luck and have fun! buckeye nation is counting on you"

    # rotate image
    with BytesIO() as output:
        with Image.open(PATH_TO_ALEX) as img:
            rotate_img= img.rotate(-days_since_start)
            rotate_img.save(output, 'jpeg')
        data = output.getvalue()

    # run image through GroupMe image service
    image_url = groupme_image_service.upload_image_data(data)

    # send message
    send_message(message_text, image_url)


if __name__ == '__main__':
    send_alex_last()
