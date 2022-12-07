import os
import requests
import logging
import time
from requests.exceptions import ConnectionError
from groupme_image_service import get_groupme_image_url_from_data_uri
from send_message import send_message
from dotenv import load_dotenv


load_dotenv()
STABLE_HORDE_API_KEY = os.environ['STABLE_HORDE_API_KEY']

MAX_CONNECTION_RETRIES = 10
MAX_DONE_CHECKS = 40
SECONDS_BETWEEN_DONE_CHECKS = 2


def draw(prompt: str) -> None:
    logging.info(f'Sending request to Stable Diffusion API (stablehorde.net) with prompt "{prompt}"')
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
    generate_response = requests.post('https://stablehorde.net/api/v2/generate/async', headers={'apikey': STABLE_HORDE_API_KEY}, json=request_body)

    if not generate_response.ok:
        logging.error(generate_response.text)
        raise Exception('Error sending initial request')

    generate_results = generate_response.json()
    logging.info(generate_results)
    image_request_id = generate_results['id']
    
    connection_retries = 0
    done_checks = 0
    is_done = False

    while not is_done and done_checks < MAX_DONE_CHECKS:
        try:
            done_checks += 1
            logging.info(f'Checking if done {done_checks}/{MAX_DONE_CHECKS}')
            check_response = requests.get(f'https://stablehorde.net/api/v2/generate/check/{image_request_id}')

            if not check_response.ok:
                logging.error(check_response.text)
                continue
            
            check_results = check_response.json()
            is_done = check_results['done']

            time.sleep(SECONDS_BETWEEN_DONE_CHECKS) # wait 2 seconds between checking if done

        except ConnectionError as e:
            connection_retries += 1
            logging.error(f'Error {e} when retrieving status. Retry {connection_retries}/{MAX_CONNECTION_RETRIES}')
            if connection_retries < MAX_CONNECTION_RETRIES:
                time.sleep(1)
                continue
            raise e

    if not is_done:
        logging.info(f'Last response: {check_response.text}')
        raise Exception(f"The image wasn't done generating after {MAX_DONE_CHECKS} checks every {SECONDS_BETWEEN_DONE_CHECKS} seconds")
    
    result_response = requests.get(f'https://stablehorde.net/api/v2/generate/status/{image_request_id}')

    if not result_response.ok:
        logging.error(result_response.text)
        raise Exception('Error getting generated image')
    
    result_json = result_response.json()
    
    if result_json['faulted']:
        raise Exception(f'Something went wrong when generating the request. Please contact the horde administrator with your request details: {request_body}')

    try:
        image_data_uri = 'data:image/webp;base64,' + result_json['generations'][0]['img']
    except e:
        logging.error(result_json)
        raise e
    
    send_message(f'here is {prompt.lower()}', image_url=get_groupme_image_url_from_data_uri(image_data_uri))        


if __name__ == '__main__':
    draw('a platypus eating sushi in Ohio Stadium hyperrealistic')
