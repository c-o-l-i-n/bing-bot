import os
import requests
import logging
import time
from groupme_image_service import get_groupme_image_url_from_url
from send_message import send_message
from dotenv import load_dotenv
from typing import Callable


load_dotenv()
STABLE_HORDE_API_KEY = os.environ['STABLE_HORDE_API_KEY']

MAX_CONNECTION_RETRIES = 10
MAX_DONE_CHECKS = 40
SECONDS_BETWEEN_REQUESTS = 2
REQUEST_TIMEOUT_SECONDS = 10


def draw(prompt: str) -> None:
    request_body = {
        'prompt': prompt,
        'params': {
            'sampler_name': 'k_lms',
            'toggles': [1, 4],
            'cfg_scale': 7.5,
            'denoising_strength': 0.75,
            'height': 512,
            'width': 512,
            'seed_variation': 1,
            'use_gfpgan': True,
            'use_real_esrgan': True,
            'use_ldsr': True,
            'use_upscaling': True,
            'steps': 100,
            'n': 1
        },
        'trusted_workers': False
    }

    logging.info(f'Sending request to Stable Diffusion API (stablehorde.net) with prompt "{prompt}"')
    image_request_id = _keep_trying_request('https://stablehorde.net/api/v2/generate/async', requests.post, {'apikey': STABLE_HORDE_API_KEY}, request_body)['id']

    logging.info('Pinging status until done')
    _keep_trying_request(f'https://stablehorde.net/api/v2/generate/check/{image_request_id}', checking_if_done=True)

    logging.info('Done! Getting results')
    results = _keep_trying_request(f'https://stablehorde.net/api/v2/generate/status/{image_request_id}')
    
    if results['faulted']:
        raise Exception(f'Something went wrong when generating the request. Please contact the horde administrator with your request details: {request_body}')

    try:
        # the api used to return bytes, now returns image url
        # image_data_uri = 'data:image/webp;base64,' + result_json['generations'][0]['img']
        image_url = results['generations'][0]['img']
    except Exception as e:
        logging.error(results)
        raise e
    
    send_message(f'here is {prompt.lower()}', image_url=get_groupme_image_url_from_url(image_url))        


def _keep_trying_request(url: str, method: Callable = requests.get, headers: dict[str, str] = None, request_body: dict = None, checking_if_done = False) -> dict:
    MAX_TRIES = MAX_DONE_CHECKS if checking_if_done else MAX_CONNECTION_RETRIES
    request_try = 0
    request_errored_out = False
    while request_try == 0 or ((request_errored_out or not response.ok or (checking_if_done and not is_done)) and request_try < MAX_TRIES):
        if request_try > 0:
            time.sleep(SECONDS_BETWEEN_REQUESTS)
        logging.info(f'Request try {request_try + 1} of {MAX_TRIES}')
        try:
            response: requests.Response = method(url, headers=headers, json=request_body, timeout=REQUEST_TIMEOUT_SECONDS)
            result = response.json()
            logging.info(result)
            if checking_if_done:
                is_done = result['done']
        except Exception as e:
            request_errored_out = True
            logging.info(f'Request errored-out: {e}')
        request_try += 1

    if not response.ok or (checking_if_done and not is_done):
        raise Exception(response.text)
    
    return result


if __name__ == '__main__':
    draw('a platypus eating sushi in Ohio Stadium hyperrealistic')
