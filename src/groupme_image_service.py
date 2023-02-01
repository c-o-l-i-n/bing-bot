import logging
import requests
from http import HTTPStatus
from io import BytesIO
from PIL import Image
from urllib.request import urlopen
from urllib.parse import quote
from tech_config import groupme_access_token


def get_groupme_image_url_from_data_uri(image_data_uri: str) -> str:
    logging.info('Converting image data URI to bytes')
    with urlopen(image_data_uri) as response:
        image_bytes = response.read()
    return get_groupme_image_url_from_bytes(image_bytes)


def get_groupme_image_url_from_bytes(image_bytes: bytes) -> str:
    logging.info('Converting image to JPEG')
    image: Image = Image.open(BytesIO(image_bytes)).convert('RGB')
    image_byte_buffer = BytesIO()
    image.save(image_byte_buffer, format='JPEG')
    image_bytes = image_byte_buffer.getvalue()

    logging.info('Uploading image data to GroupMe image service')

    response = requests.post(url='https://image.groupme.com/pictures',
                        data=image_bytes,
                        headers={'Content-Type': 'image/jpeg',
                                'X-Access-Token': groupme_access_token()})

    if response.status_code != HTTPStatus.OK:
        logging.error(response.text)
        raise Exception('Error uploading image to GroupMe Image Service. Either something is wrong with this particular image, or an external service (Imgflip, AllOrigins, GroupMe Image Service, etc) is not working.')

    groupme_image_url = response.json()['payload']['picture_url']
    logging.info(f'Image uploaded to {groupme_image_url}')

    return groupme_image_url


def get_groupme_image_url_from_url(image_url: str) -> str:
    logging.info(f'Uploading image URL to GroupMe image service: {image_url}')
    encoded_image_url = quote(image_url, safe='')
    image_data = requests.get(f'https://api.allorigins.win/raw?url={encoded_image_url}').content
    return get_groupme_image_url_from_bytes(image_data)
