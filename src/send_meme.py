from send_message import send_message
import random
import json
from urllib.request import Request, urlopen
import requests
from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
import fix_path
import groupme_image_service
import random
import secrets


def get_random_meme_url():
    MEME_IDS = [
        112126428,
        181913649,
        87743020,
        438680,
        61579,
        102156234,
        129242436,
        93895088,
        124822590,
        101470,
        1035805,
        61520,
        4087833,
        89370399,
        91538330,
        119139145,
        188390779,
        61532,
        131087935,
        61585,
        5496396,
        61539,
        155067746,
        8072285,
        97984,
        217743513,
        21735,
        100777631,
        124055727,
        114585149,
        61527,
        28251713,
        123999232,
        27813981,
        563423,
        101288,
        61546,
        61582,
        235589,
        134797956,
        6235864,
        61533,
        16464531,
        405658,
        1509839,
        178591752,
        101511,
        91545132,
        61556,
        14371066,
        14230520,
        100947,
        101287,
        245898,
        61544,
        175540452,
        61516,
        84341851,
        101440,
        148909805,
        135256802,
        922147,
        222403160,
        259680,
        161865971,
        135678846,
        40945639,
        61580,
        101910402,
        196652226,
        132769734,
        101716,
        9440985,
        109765,
        61581,
        226297822,
        80707627,
        12403754,
        56225174,
        3218037,
        195389,
        766986,
        100955,
        444501,
        21604248,
        718432,
        163573,
        124212,
        13757816,
        143601,
        61583,
        460541,
        1790995,
        442575,
        6531067,
        180190441,
        101711,
        1367068,
        29617627,
        10628640,
    ]

    meme_text = 'H'

    text_option = random.randrange(3)
    # 0: only text0 (top text)
    # 1: only text1 (bottom text)
    # 2: both text0 and text1

    api_url = f'http://api.imgflip.com/caption_image?template_id={str(random.choice(MEME_IDS))}&username=bing_bot&password=vzhOzeCWmmZjhhvOpPOZOezgbDIkHyKJATWWvujmpetJrBSdpS{f"&text0={meme_text}" if text_option % 2 == 0 else ""}{f"&text1={meme_text}" if text_option > 0 else ""}'

    response = requests.post(
        api_url, headers={'User-Agent': 'Mozilla/5.0'}).json()

    if response['success']:
        api_image_url = response['data']['url']
        return api_image_url


def deep_fry_image(image_url):
    image = Image.open(requests.get(image_url, stream=True).raw)
    laugh_image = Image.open(secrets.PATH_TO_LAUGH, 'r')

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


def send_meme(message_text=None, is_deep_fried=False):
    api_image_url = get_random_meme_url()
    if is_deep_fried:
        image_byte_array = BytesIO()
        deep_fry_image(api_image_url).save(image_byte_array, format='png')
        image_byte_array = image_byte_array.getvalue()
        groupme_image_url = groupme_image_service.upload_image_data(
            image_byte_array)
    else:
        groupme_image_url = groupme_image_service.upload_image_url(
            api_image_url)
    send_message(message_text, groupme_image_url)


if __name__ == '__main__':
    send_meme(is_deep_fried=True)
