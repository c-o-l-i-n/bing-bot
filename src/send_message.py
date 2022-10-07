import logging
import requests
from tech_config import groupme_bot_id


def send_message(text, image_url=None):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id'      : groupme_bot_id(),
        'text'        : text if text else '',
        'picture_url' : image_url if image_url else '',
    }

    logging.info(f'Sending message: {data}')

    response = requests.post(url, json=data)

    if response.status_code != 202:
        logging.error(response.text)