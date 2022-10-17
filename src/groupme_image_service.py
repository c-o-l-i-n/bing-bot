import logging
import requests
from http import HTTPStatus
from io import BytesIO
from urllib.request import urlopen
from send_message import send_message
from tech_config import groupme_access_token


def get_groupme_image_url_from_data_uri(image_data_uri: str) -> str:
    with urlopen(image_data_uri) as response:
        image_bytes = response.read()
    return get_groupme_image_url_from_bytes(image_bytes)


def get_groupme_image_url_from_bytes(image_bytes: bytes) -> str:
    logging.info('Uploading image data to GroupMe image service')

    response = requests.post(url='https://image.groupme.com/pictures',
                        data=image_bytes,
                        headers={'Content-Type': 'image/jpeg',
                                'X-Access-Token': groupme_access_token()})

    if response.status_code != HTTPStatus.OK:
        logging.error(response.text)
        return '' 

    groupme_image_url = response.json()['payload']['picture_url']
    logging.info(f'Image uploaded to {groupme_image_url}')

    return groupme_image_url


def get_groupme_image_url_from_url(image_url: str) -> str:
    logging.info(f'Uploading image URL to GroupMe image service: {image_url}')
    image_data = BytesIO(requests.get(f'https://api.allorigins.win/raw?url={image_url}').content)
    return get_groupme_image_url_from_bytes(image_data)
