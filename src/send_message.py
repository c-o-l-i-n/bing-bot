import os
import requests
import fix_path


GROUPME_BOT_ID = os.environ['GROUPME_BOT_ID']


def send_message(text, image_url=None):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id'      : GROUPME_BOT_ID,
        'text'        : text if text else '',
        'picture_url' : image_url if image_url else '',
    }

    requests.post(url, json=data)
