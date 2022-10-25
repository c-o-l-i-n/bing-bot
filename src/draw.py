import os
import requests
import logging
from groupme_image_service import get_groupme_image_url_from_data_uri
from send_message import send_message
from dotenv import load_dotenv


load_dotenv()
STABLE_HORDE_API_KEY = os.environ['STABLE_HORDE_API_KEY']


def draw(prompt: str) -> None:
    logging.info(f'Sending request to Stable Diffusion API (stablehorde.net) with prompt "{prompt}"')
    response = requests.post('https://stablehorde.net/api/v2/generate/sync', headers={'apikey': STABLE_HORDE_API_KEY}, json={
        "prompt": prompt,
        "params": {
            "sampler_name": "k_lms",
            "toggles": [1, 4],
            "cfg_scale": 7.5,
            "denoising_strength": 0.75,
            "height": 512,
            "width": 512,
            "seed_variation": 1,
            "use_gfpgan": True,
            "use_real_esrgan": True,
            "use_ldsr": True,
            "use_upscaling": True,
            "steps": 100,
            "n": 1
        },
        "trusted_workers": False
    }).json()
    logging.info('Received reponse')
    image_data_uri = 'data:image/webp;base64,' + response['generations'][0]['img']
    send_message(f'here is {prompt.lower()}', image_url=get_groupme_image_url_from_data_uri(image_data_uri))


if __name__ == "__main__":
    draw('a platypus eating sushi in Ohio Stadium hyperrealistic')
