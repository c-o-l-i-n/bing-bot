import os
import logging
from send_message import send_message
import random
import requests
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
from PIL.Image import Image as ImageType
import groupme_image_service
import random
from cachetools import cached, TTLCache
from dotenv import load_dotenv


load_dotenv()
IMGFLIP_API_KEY = os.environ['IMGFLIP_API_KEY']
BACKUP_MEME_TEMPLATES = ['181913649', '87743020', '112126428', '131087935', '129242436', '217743513', '124822590', '247375501', '222403160', '131940431', '4087833', '135256802', '80707627', '438680', '93895088', '252600902', '188390779', '97984', '119139145', '27813981', '61579', '178591752', '101470', '1035805', '102156234', '110163934', '91538330', '79132341', '195515965', '148909805', '161865971', '216951317', '180190441', '226297822', '100777631', '114585149', '3218037', '55311130', '124055727', '89370399', '134797956', '61520', '61556', '123999232', '99683372', '21735', '28251713', '5496396', '135678846', '155067746', '259237855', '6235864', '84341851', '132769734', '175540452', '101288', '196652226', '91545132', '8072285', '61544', '61532', '17496002', '563423', '29617627', '163573', '14371066', '61546', '24557067', '460541', '61539', '101716', '6531067', '1367068', '29562797', '142921050', '285870', '101511', '61585', '7183956', '61580', '61533', '101910402', '16464531', '8279814', '183518946', '21604248', '922147', '176908', '405658', '89655', '61527', '1464444', '56225174', '1202623', '61516', '101287', '61581', '28034788', '71428573', '371382']


# cache current popular meme templates, ttl 1 day
@cached(TTLCache(maxsize=1, ttl=60 * 60 * 24))
def _get_current_popular_meme_templates() -> list[str]:
    logging.info('Getting current top 100 meme templates')
    meme_templates = []
    try:
        meme_templates = list(map(lambda x : x['id'], requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']))
    except Exception as e:
        logging.error(e)
        logging.error('Error getting meme templates. Reverting to backup:')
        meme_templates = BACKUP_MEME_TEMPLATES
    logging.info(meme_templates)
    return meme_templates


def _get_meme_text() -> str:
    return random.choice(['H', 'H', 'H', 'piss', 'ohio', 'baritone'])


def _get_random_meme_url() -> str:
    meme_teamplate = random.choice(_get_current_popular_meme_templates())

    text_option = random.randrange(3)
    # 0: only top text
    # 1: only bottom text
    # 2: both top and bottom text

    top_text = _get_meme_text() if text_option % 2 == 0 else ''
    bottom_text = _get_meme_text() if text_option > 0 else ''

    api_url = f'https://api.imgflip.com/caption_image?template_id={meme_teamplate}&username=bing_bot&password={IMGFLIP_API_KEY}&text0={top_text}&text1={bottom_text}'

    logging.info(f'Getting meme (template ID: {meme_teamplate}) from Imgflip')
    response = requests.post(
        api_url, headers={'User-Agent': 'Mozilla/5.0'}).json()

    if response['success']:
        meme_image_url = response['data']['url']
        logging.info(f'Meme image URL: {meme_image_url}')
        return meme_image_url
    else:
        logging.error(response)
        raise Exception('Error getting meme image')


def _deep_fry_image(image_url) -> ImageType:
    logging.info('Deep frying image')
    image = Image.open(requests.get(f'https://api.allorigins.win/raw?url={image_url}', stream=True).raw)
    laugh_image = Image.open(Path(__file__).parent / '../../assets/laugh.png', 'r')

    laugh_size = laugh_image.size[0]

    img_w, img_h = image.size

    random_position = (random.randrange(0, img_w - laugh_size),
                       random.randrange(0, img_h - laugh_size))

    image.paste(laugh_image, random_position)

    # super edge enhance
    for _ in range(3):
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # "enhance" color
    converter = ImageEnhance.Color(image)
    converter2 = ImageEnhance.Contrast(image)
    image = converter.enhance(100)
    image = converter2.enhance(100)

    return image


def send_meme(message_text=None, is_deep_fried=False) -> None:
    api_image_url = _get_random_meme_url()
    if is_deep_fried:
        image_bytes_buffer = BytesIO()
        _deep_fry_image(api_image_url).save(image_bytes_buffer, format='jpeg')
        image_bytes = image_bytes_buffer.getvalue()
        groupme_image_url = groupme_image_service.get_groupme_image_url_from_bytes(image_bytes)
    else:
        groupme_image_url = groupme_image_service.get_groupme_image_url_from_url(api_image_url)
    send_message(message_text, groupme_image_url)


def send_normal_or_deep_fried_meme() -> None:
    is_deep_fried = random.random() < 0.3
    send_meme(is_deep_fried=is_deep_fried)


if __name__ == '__main__':
    send_meme(is_deep_fried=True)
