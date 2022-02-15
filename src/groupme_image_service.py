import requests
import base64
from secrets import ACCESS_TOKEN
from io import BytesIO
from PIL import Image

def upload_image_data(image_data):
    response = requests.post(url='https://image.groupme.com/pictures',
                        data=image_data,
                        headers={'Content-Type': 'image/jpeg',
                                'X-Access-Token': ACCESS_TOKEN}).json()
    groupme_image_url = response['payload']['picture_url']
    return groupme_image_url


def upload_image_url(url):
    image_data = BytesIO(requests.get(url).content)
    return upload_image_data(image_data)
