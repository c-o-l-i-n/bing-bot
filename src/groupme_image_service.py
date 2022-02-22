import os
import logging
import requests
from io import BytesIO


GROUPME_ACCESS_TOKEN = os.environ['GROUPME_ACCESS_TOKEN']


def upload_image_data(image_data):
    logging.info('Uploading image data to GroupMe image service')

    response = requests.post(url='https://image.groupme.com/pictures',
                        data=image_data,
                        headers={'Content-Type': 'image/jpeg',
                                'X-Access-Token': GROUPME_ACCESS_TOKEN})

    if response.status_code != 200:
        logging.error(response.text)
        return '' 

    groupme_image_url = response.json()['payload']['picture_url']
    logging.info(f'Image uploaded to {groupme_image_url}')

    return groupme_image_url


def upload_image_url(url):
    logging.info(f'Uploading image URL to GroupMe image service: {url}')
    image_data = BytesIO(requests.get(url).content)
    return upload_image_data(image_data)
