import logging.config

# set logging config before importing other files that use logging
logging.config.fileConfig('logging.conf')

import logging
import requests
from http import HTTPStatus
from cachetools import cached, TTLCache
from flask import Flask, request
from nicknames import create_new_nickname, get_nicknames as nicknames
from send_message import send_message
from settings import Command, UnsolicitedMessage, get_settings
from weather import get_weather, get_temperature
from image_recognition import identify_image
from groupme_image_service import upload_image_url
from randomize_unsolicited_message_times import randomize_unsolicited_message_times
from college_football import send_go_ohio, set_go_ohio_date_and_time
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


def message_contains(text: str, message: str) -> bool:
    return text.lower() in message.lower()


# cache settings, ttl 10 minutes
@cached(TTLCache(maxsize=128, ttl=10 * 60))
def settings():
    return get_settings()


# GroupMe message callback
@app.route('/', methods=['POST'])
def receive_message():
    logging.info(f'Message received')

    # get message data
    data = request.get_json()
    message = data['text']
    name = data['name']
    sender_id = data['sender_id']
    sender_type = data['sender_type']
    image_attachment_urls = list(map(lambda i: i['url'], filter(lambda a: a['type'] == 'image', data['attachments'])))

    if sender_type != 'user':
        logging.info(f'From {sender_type}')
        return '', HTTPStatus.NO_CONTENT
    
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
        if settings()[Command.MAKE_MEME] and message_contains('meme', message):
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

        # uses computer vision to identify what's in an image
        if settings()[Command.WHAT_IS_THIS] and (message_contains('what is this', message) or message_contains("what's this", message) or message_contains('what this is', message) or message_contains('think this is', message)):
            if len(image_attachment_urls) > 0:
                send_message(identify_image(image_attachment_urls[0]))
            else:
                send_message('you gotta send me a picture ya dingus')

        # sends a random picture of a dog
        if settings()[Command.DOG] and (message_contains('dog', message)):
            cat_image_url = requests.get('https://dog.ceo/api/breeds/image/random').json()['message']
            send_message('', image_url=upload_image_url(cat_image_url))

        # sends a random picture of a cat
        if settings()[Command.CAT] and (message_contains('cat', message)):
            cat_image_url = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
            send_message('', image_url=upload_image_url(cat_image_url))

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

    # suggests an activity if you're bored
    if settings()[Command.BORED] and message_contains('bored', message):
        activity = requests.get('https://www.boredapi.com/api/activity').json()['activity'].lower()
        send_message(f'you should {activity}')
    
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
    UnsolicitedMessage.WAWA: send_call_wawa,
    UnsolicitedMessage.GO_OHIO: send_go_ohio
}


# triggered by cron jobs from cron-job.org
@app.route('/send', methods=['GET'])
def send_unsolicited_message():
    unsolicited_message = UnsolicitedMessage(request.args.get('m'))
    logging.info(f'Recieved request to send unsolicited message {unsolicited_message.name}')
    
    if settings()[unsolicited_message]:
        UNSOLICITED_MESSAGE_FUNCTIONS[unsolicited_message]()
    else:
        logging.info('Setting turned off. No message sent.')

    return '', HTTPStatus.NO_CONTENT
    

# randomize unsolictied message times
# triggered every morning by cron-job.org
@app.route('/randomize', methods=['GET'])
def randomize():
    logging.info('Received request to randomize unsolicited message cron job times')
    randomize_unsolicited_message_times()
    return '', HTTPStatus.NO_CONTENT
    

# sets time to send go ohio to 3 hours before kickoff
# triggered every Friday morning from August to January by cron-job.org
@app.route('/set-go-ohio', methods=['GET'])
def set_go_ohio():
    logging.info(f'Recieved request to set GO_OHIO date and time')
    set_go_ohio_date_and_time()
    return '', HTTPStatus.NO_CONTENT
    

# index webpage
@app.route('/', methods=['GET'])
def get_index_page():
    logging.info(f'Serving index page')
    return '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🦏 Bing Bot</title>
            </head>
            <body style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;margin:0">
                <h1 style="font-family:sans-serif;text-align:center">
                    🦏👋 Hello from Bing's server!
                </h1>
                <iframe width="560" height="315" src="https://www.youtube.com/embed/b-nwRDNoJR4?autoplay=1&controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                <h2 style="font-family:sans-serif;text-align:center">
                    ✅ Bing Bot is up and running
                </h2>
                <p style="font-family:sans-serif;text-align:center;margin-top:0">
                    Something wrong? Check the <a href="https://go.osu.edu/binghelp">help guide</a>
                </p>
            </body>
        </html>'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
