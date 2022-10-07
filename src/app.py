import os
import logging
import logging.config
import requests
from pathlib import Path
from cachetools import cached, TTLCache
from flask import Flask, request
from waitress import serve


# set logging config
logging.config.fileConfig('logging.conf')

# set up google credentials
logging.info('Setting up credentials.json')
with open(Path(__file__).parent / '../credentials.json', 'w') as credentials_file:
    credentials_file.write(os.environ['CREDENTIALS_JSON'])


from nicknames import create_new_nickname, get_nicknames as nicknames
from send_message import send_message
from settings import CommandSetting, get_settings
from weather import get_weather, get_temperature
from custom_message_senders.send_the_car_quote import send_the_car_quote
from custom_message_senders.send_meme import send_meme


# set logging config
logging.config.fileConfig('logging.conf')#(format='%(levelname)s: %(message)s', level=logging.INFO)


# initialize Flask app
logging.info('Creating Flask app')
app = Flask(__name__)


def message_contains(text, message):
    return text.lower() in message.lower()


# cache settings, ttl 10 minutes
@cached(TTLCache(maxsize=128, ttl=10 * 60))
def settings():
    return get_settings()


@app.route('/bing', methods=['POST'])
def receive_message():
    logging.info(f'Message received')

    # get message data
    try:
        data = request.get_json()
        message = data['text']
        name = data['name']
        sender_id = data['sender_id']
        sender_type = data['sender_type']
    except:
        return

    if sender_type != 'user':
        logging.info(f'From {sender_type}')
        return "ok", 200
    
    logging.info(f'From {name} ({sender_id}): {message}')

    if not sender_id in nicknames():
        logging.info('Never seen message by this user before. Adding to Nicknames spreadsheet.')
        sender_first_name = name.split(' ')[0].lower()
        create_new_nickname(sender_id, sender_first_name)
        send_message(f'nice to meet you, {sender_first_name}!')

    if message_contains('bing', message):
        # a message to confirm that bing is up and running
        if settings()[CommandSetting.ARE_YOU_ALIVE] and message_contains('are you alive', message):
            send_message('yeah')

        # says 'hi' back to sender, and includes name if they're in H-Row
        if settings()[CommandSetting.HI] and (message_contains('hi bing', message) or message_contains('hi, bing', message)):
            new_message = 'hi'
            if sender_id in nicknames():
                new_message += f' {nicknames()[sender_id]}'
            send_message(new_message)

        # says 'i love you' back to sender, and includes name if they're in H-Row
        if settings()[CommandSetting.I_LOVE_YOU] and message_contains('i love you', message):
            new_message = 'i love you too'
            if sender_id in nicknames():
                new_message += f' {nicknames()[sender_id]}'
            send_message(new_message)

        # tells a joke on demand
        if settings()[CommandSetting.JOKE] and message_contains('joke', message):
            send_message(requests.get('https://icanhazdadjoke.com/',
                                      headers={'Accept': 'text/plain'}).text[:-1].lower())

        # gets weather on demand
        if settings()[CommandSetting.WEATHER] and message_contains('weather', message):
            send_message(get_weather())

        # gets temperature on demand
        if settings()[CommandSetting.TEMPERATURE] and message_contains('temperature', message):
            temperature = get_temperature()
            send_message(
                f'{temperature}{" (nice)" if "69" in temperature else ""}')

        # make a new meme on demand
        if settings()[CommandSetting.MAKE_MEME] and ((message_contains('make', message) or message_contains('send', message)) and message_contains('meme', message)):
            if sender_id in nicknames():
                message_text = f'''ok {nicknames()[data["sender_id"]]}, here's a new meme'''
            else:
                message_text = f'''ok, here's a new meme'''
            if message_contains('deep fried', message):
                send_meme(message_text=message_text, is_deep_fried=True)
            else:
                send_meme(message_text=message_text)

        # gives a random recipe
        if settings()[CommandSetting.COOK_MEAL] and (message_contains('cook', message) or message_contains('meal', message) or message_contains('dinner', message) or message_contains('lunch', message)):
            recipe = requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php').json()
            send_message(f'you should have {recipe["meals"][0]["strMeal"].lower()}' + (("\n\n" + recipe['meals'][0]['strYoutube']) if recipe["meals"]
                                                                                       [0]["strYoutube"] else "") + (("\n\n" + recipe['meals'][0]['strSource']) if recipe["meals"][0]["strSource"] else ""))

        # sends a quote from the movie "The Car"
        if settings()[CommandSetting.THE_CAR_QUOTE] and (message_contains('car', message) and (message_contains('line', message) or message_contains('quote', message))):
            send_the_car_quote()

    # has something for the good of the order
    if settings()[CommandSetting.GOOD_OF_THE_ORDER] and message_contains('good of the order', message):
        send_message('tits')

    # sings "One Pizza Pie"
    if settings()[CommandSetting.ONE_PIZZA_PIE] and ('one pizza pie' == message[-13:].lower() or 'one pizza pie' == message[-14:-1].lower() or '1 pizza pie' == message[-11:].lower() or '1 for me' == message[-12:-1].lower()):
        send_message('🍕 one for me, 🍕 one for when i die')

    # sings "One Pizza Pie"
    if settings()[CommandSetting.ONE_PIZZA_PIE] and ('one for me' == message[-10:].lower() or 'one for me' == message[-11:-1].lower() or '1 for me' == message[-8:].lower() or '1 for me' == message[-9:-1].lower()):
        send_message('🍕 one for when i die')

    # says "nice" when someone else says 69 or 420
    if settings()[CommandSetting.FUNNY_NUMBERS] and ((message_contains('69', message) or message_contains('420', message))):
        send_message('nice')

    # says "ass" after "h"
    if settings()[CommandSetting.HAOUS] and 'h' == message.lower():
        send_message('ass')

    # says "ohio" after "ass"
    if settings()[CommandSetting.HAOUS] and 'ass' == message.lower():
        send_message('ohio')

    # says "you suck" after "ohio"
    if settings()[CommandSetting.HAOUS] and 'ohio' == message.lower():
        send_message('you suck!')

    # says "ohio, you suck" after "h, ass"
    if settings()[CommandSetting.HAOUS] and ('h ass' == message[-5:].lower() or 'h, ass' == message[-6:].lower()):
        send_message('ohio, you suck!')
    
    return "ok", 200


@app.route('/', methods=['GET'])
def get():
    logging.info(f'Serving index page')
    return '''
        <body style="display:flex;justify-content:center;align-items:center">
            <h1 style="font-family:sans-serif;text-align:center">
                🦏👋 Hello from Bing's server!
            </h1>
        </body>'''



if __name__ == '__main__':
    serve(app, port=8080)
