import os
import logging
import logging.config
import requests
from http import HTTPStatus
from pathlib import Path
from cachetools import cached, TTLCache
from flask import Flask, request


# set logging config
logging.config.fileConfig('logging.conf')

# set up google credentials
logging.info('Setting up credentials.json')
with open(Path(__file__).parent / '../credentials.json', 'w') as credentials_file:
    credentials_file.write(os.environ['CREDENTIALS_JSON'])


from nicknames import create_new_nickname, get_nicknames as nicknames
from send_message import send_message
from settings import Command, UnsolicitedMessage, get_settings
from weather import get_weather, get_temperature
from custom_message_senders.send_the_car_quote import send_the_car_quote
from custom_message_senders.send_meme import send_meme
from custom_message_senders.send_air_piss import send_air_piss
from custom_message_senders.send_alex import send_alex
from custom_message_senders.send_call_wawa import send_call_wawa
from custom_message_senders.send_drink_water import send_drink_water
from custom_message_senders.send_elon import send_elon
from custom_message_senders.send_h import send_h
from custom_message_senders.send_now_you_see_me import send_now_you_see_me
from custom_message_senders.send_sky_piss import send_sky_piss


# initialize Flask app
logging.info('Creating Flask app')
app = Flask(__name__)


def message_contains(text, message):
    return text.lower() in message.lower()


# cache settings, ttl 10 minutes
@cached(TTLCache(maxsize=128, ttl=10 * 60))
def settings():
    return get_settings()


@app.route('/', methods=['POST'])
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
        if settings()[Command.ARE_YOU_ALIVE] and message_contains('are you alive', message):
            send_message('yeah')

        # says 'hi' back to sender, and includes name if they're in H-Row
        if settings()[Command.HI] and (message_contains('hi bing', message) or message_contains('hi, bing', message)):
            new_message = 'hi'
            if sender_id in nicknames():
                new_message += f' {nicknames()[sender_id]}'
            send_message(new_message)

        # says 'i love you' back to sender, and includes name if they're in H-Row
        if settings()[Command.I_LOVE_YOU] and message_contains('i love you', message):
            new_message = 'i love you too'
            if sender_id in nicknames():
                new_message += f' {nicknames()[sender_id]}'
            send_message(new_message)

        # tells a joke on demand
        if settings()[Command.JOKE] and message_contains('joke', message):
            send_message(requests.get('https://icanhazdadjoke.com/',
                                      headers={'Accept': 'text/plain'}).text[:-1].lower())

        # gets weather on demand
        if settings()[Command.WEATHER] and message_contains('weather', message):
            send_message(get_weather())

        # gets temperature on demand
        if settings()[Command.TEMPERATURE] and message_contains('temperature', message):
            temperature = get_temperature()
            send_message(
                f'{temperature}{" (nice)" if "69" in temperature else ""}')

        # make a new meme on demand
        if settings()[Command.MAKE_MEME] and ((message_contains('make', message) or message_contains('send', message)) and message_contains('meme', message)):
            if sender_id in nicknames():
                message_text = f'''ok {nicknames()[data["sender_id"]]}, here's a new meme'''
            else:
                message_text = f'''ok, here's a new meme'''
            if message_contains('deep fried', message):
                send_meme(message_text=message_text, is_deep_fried=True)
            else:
                send_meme(message_text=message_text)

        # gives a random recipe
        if settings()[Command.COOK_MEAL] and (message_contains('cook', message) or message_contains('meal', message) or message_contains('dinner', message) or message_contains('lunch', message)):
            recipe = requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php').json()
            send_message(f'you should have {recipe["meals"][0]["strMeal"].lower()}' + (("\n\n" + recipe['meals'][0]['strYoutube']) if recipe["meals"]
                                                                                       [0]["strYoutube"] else "") + (("\n\n" + recipe['meals'][0]['strSource']) if recipe["meals"][0]["strSource"] else ""))

        # sends a quote from the movie "The Car"
        if settings()[Command.THE_CAR_QUOTE] and (message_contains('car', message) and (message_contains('line', message) or message_contains('quote', message))):
            send_the_car_quote(is_quote_of_the_day=False)

        # get help links
        if message_contains('help', message) or message_contains('settings', message) or (message_contains('change', message) and message_contains('name', message)) or message_contains('nickname', message):
            send_message('change settings and nicknames here:\ngo.osu.edu/bingsettings\n\nread more here:\ngo.osu.edu/binghelp')
        

    # has something for the good of the order
    if settings()[Command.GOOD_OF_THE_ORDER] and message_contains('good of the order', message):
        send_message('tits')

    # sings "One Pizza Pie"
    if settings()[Command.ONE_PIZZA_PIE] and ('one pizza pie' == message[-13:].lower() or 'one pizza pie' == message[-14:-1].lower() or '1 pizza pie' == message[-11:].lower() or '1 for me' == message[-12:-1].lower()):
        send_message('🍕 one for me, 🍕 one for when i die')

    # sings "One Pizza Pie"
    if settings()[Command.ONE_PIZZA_PIE] and ('one for me' == message[-10:].lower() or 'one for me' == message[-11:-1].lower() or '1 for me' == message[-8:].lower() or '1 for me' == message[-9:-1].lower()):
        send_message('🍕 one for when i die')

    # says "nice" when someone else says 69 or 420
    if settings()[Command.FUNNY_NUMBERS] and ((message_contains('69', message) or message_contains('420', message))):
        send_message('nice')

    # says "ass" after "h"
    if settings()[Command.HAOUS] and 'h' == message.lower():
        send_message('ass')

    # says "ohio" after "ass"
    if settings()[Command.HAOUS] and 'ass' == message.lower():
        send_message('ohio')

    # says "you suck" after "ohio"
    if settings()[Command.HAOUS] and 'ohio' == message.lower():
        send_message('you suck!')

    # says "ohio, you suck" after "h, ass"
    if settings()[Command.HAOUS] and ('h ass' == message[-5:].lower() or 'h, ass' == message[-6:].lower()):
        send_message('ohio, you suck!')
    
    return '', HTTPStatus.NO_CONTENT


UNSOLICITED_MESSAGE_FUNCTIONS = {
    UnsolicitedMessage.ELON_MUSK: send_elon,
    UnsolicitedMessage.H: send_h,
    UnsolicitedMessage.HANNA_DRINK_WATER: send_drink_water,
    UnsolicitedMessage.HUMIDITY: send_air_piss,
    UnsolicitedMessage.MEME: send_meme,
    UnsolicitedMessage.NOW_YOU_SEE_ME: send_now_you_see_me,
    UnsolicitedMessage.RAIN: send_sky_piss,
    UnsolicitedMessage.ROTATE_ALEX: send_alex,
    UnsolicitedMessage.THE_CAR_QUOTE: send_the_car_quote,
    UnsolicitedMessage.WAWA: send_call_wawa
}


# I know this isn't the proper semantic use of a HEAD request, but it works nicely
@app.route('/', methods=['HEAD'])
def send_unsolicited_message():
    unsolicited_message = UnsolicitedMessage(int(request.args.get('type')))
    logging.info(f'Recieved request to send unsolicited message {unsolicited_message.name}')
    
    if settings()[unsolicited_message]:
        UNSOLICITED_MESSAGE_FUNCTIONS[unsolicited_message]()

    return '', HTTPStatus.NO_CONTENT
    

@app.route('/', methods=['GET'])
def get_index_page():
    logging.info(f'Serving index page')
    return '''
        <body style="display:flex;justify-content:center;align-items:center">
            <h1 style="font-family:sans-serif;text-align:center">
                🦏👋 Hello from Bing's server!
            </h1>
        </body>'''


if __name__ == '__main__':
    app.run()
