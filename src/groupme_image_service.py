from http import HTTPStatus
import logging
import requests
from io import BytesIO
from tech_config import groupme_access_token



def upload_image_data(image_data):
    logging.info('Uploading image data to GroupMe image service')

    response = requests.post(url='https://image.groupme.com/pictures',
                        data=image_data,
                        headers={'Content-Type': 'image/jpeg',
                                'X-Access-Token': groupme_access_token()})

    if response.status_code != HTTPStatus.OK:
        logging.error(response.text)
        return '' 

    groupme_image_url = response.json()['payload']['picture_url']
    logging.info(f'Image uploaded to {groupme_image_url}')

    return groupme_image_url


def upload_image_url(url):
    logging.info(f'Uploading image URL to GroupMe image service: {url}')
    image_data = BytesIO(requests.get(f'https://api.allorigins.win/raw?url={url}').content)
    return upload_image_data(image_data)
