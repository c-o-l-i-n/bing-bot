import os
import requests
from io import BytesIO


GROUPME_ACCESS_TOKEN = os.environ['GROUPME_ACCESS_TOKEN']


def upload_image_data(image_data):
    response = requests.post(url='https://image.groupme.com/pictures',
                        data=image_data,
                        headers={'Content-Type': 'image/jpeg',
                                'X-Access-Token': GROUPME_ACCESS_TOKEN}).json()
    groupme_image_url = response['payload']['picture_url']
    return groupme_image_url


def upload_image_url(url):
    image_data = BytesIO(requests.get(url).content)
    return upload_image_data(image_data)
