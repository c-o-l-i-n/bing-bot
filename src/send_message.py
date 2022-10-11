import logging
import requests
from tech_config import groupme_bot_id
from http import HTTPStatus


def send_message(text: str, image_url: str='') -> None:
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id'      : groupme_bot_id(),
        'text'        : text,
        'picture_url' : image_url,
    }

    logging.info(f'Sending message: {data}')

    response = requests.post(url, json=data)

    if response.status_code != HTTPStatus.ACCEPTED:
        logging.error(response.text)