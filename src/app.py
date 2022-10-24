import logging.config

# set logging config before importing other files that use logging
logging.config.fileConfig('logging.conf')

import logging
import requests
import re
from http import HTTPStatus
from datetime import datetime
from cachetools import cached, TTLCache
from flask import Flask, request
from nicknames import create_new_nickname, get_nicknames as nicknames
from send_message import send_message
from settings import Command, UnsolicitedMessage, get_settings
from weather import get_weather, get_temperature
from image_recognition import identify_image
from groupme_image_service import get_groupme_image_url_from_data_uri, get_groupme_image_url_from_url
from cron import randomize_unsolicited_message_times
from college_football import send_beating_next, send_bing_10_picks, send_go_ohio, set_game_day_messages_date_and_time
from draw import draw
from custom_message_senders.send_hello import send_hello
from custom_message_senders.send_the_car_quote import send_the_car_quote
from custom_message_senders.send_meme import send_meme, send_normal_or_deep_fried_meme
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
    return text.lower() in message.lower().replace("’", "'")


# cache settings, ttl 10 minutes
@cached(TTLCache(maxsize=128, ttl=10 * 60))
def settings():
    return get_settings()


# GroupMe message callback
@app.route('/', methods=['POST'])
def receive_message():
    logging.info(f'Message received')

    # get message data
    data: dict = request.get_json()
    message: str = data['text']
    name: str = data['name']
    sender_id: str = data['sender_id']
    sender_type: str = data['sender_type']
    image_attachment_urls: list[str] = list(map(lambda i: i['url'], filter(lambda a: a['type'] == 'image', data['attachments'])))

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
            new_message += f' {nicknames()[sender_id]}'
            send_message(new_message)

        # says 'i love you' back to sender, and includes name if they're in H-Row
        if settings()[Command.I_LOVE_YOU] and message_contains('i love you', message):
            send_message(f'i love you too {nicknames()[sender_id]}')

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
            message_text = f'''ok {nicknames()[sender_id]}, here's a new meme'''
            try:
                if message_contains('deep fried', message):
                    send_meme(message_text=message_text, is_deep_fried=True)
                else:
                    send_meme(message_text=message_text)
            except:
                send_message('no')

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
        if settings()[Command.WHAT_IS_THIS] and (message_contains('what is this', message) or message_contains("what's this", message) or message_contains("what's this", message) or message_contains('what this is', message) or message_contains('think this is', message)):
            if len(image_attachment_urls) > 0:
                send_message(identify_image(image_attachment_urls[0]))
            else:
                send_message('you gotta send me a picture ya dingus')

        # sends a random picture of a dog
        if settings()[Command.DOG] and (message_contains('dog', message)):
            cat_image_url = requests.get('https://dog.ceo/api/breeds/image/random').json()['message']
            send_message('', image_url=get_groupme_image_url_from_url(cat_image_url))

        # sends a random picture of a cat
        if settings()[Command.CAT] and (message_contains('cat', message)):
            cat_image_url = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
            send_message('', image_url=get_groupme_image_url_from_url(cat_image_url))

        # use ai to generate an image based on a text prompt
        if settings()[Command.DRAW]:
            word = 'draw'
            draw_pattern = fr'\b{word}\b'
            draw_pattern_result = re.search(draw_pattern, message.lower())
            if draw_pattern_result:
                prompt = message[draw_pattern_result.start() + len(word) + 1:].strip()
                if prompt:
                    send_message(f"ok {nicknames()[sender_id]}, gimme just a sec...")
                    image_data_uri = draw(prompt)
                    try:
                        picture_url = get_groupme_image_url_from_data_uri(image_data_uri)
                    except:
                        send_message('sorry, my pencil broke :(')
                    
                    if image_data_uri:
                        send_message(f'here is {prompt.lower()}', picture_url)
                    else:
                        send_message('sorry, my pencil broke :(')
                else:
                    send_message('tell me what to draw. try something like:\n"bing draw a platypus eating sushi in ohio stadium"\n"bing draw shrek playing a saxophone at the disco"\n"bing draw a giant lasagna in the middle of new york city"\n"bing draw princess elsa and spider-man leading an army of angry flaming skeleton soldiers from hell hyperrealistic"', get_groupme_image_url_from_url('https://i.imgur.com/X8gipGC.jpg'))

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

    if settings()[Command.COME]:
        # who doesn't love a good regular expression?
        come_pattern = r'\b(come|comes|coming|came|finish|finishes|finishing|finished)\b'
        come_result = re.search(come_pattern, message.lower())
        if come_result:
            if re.search(fr'\b(i|you|we) {come_pattern}', message.lower()):
                send_message('you WHAT??')
            elif re.search(fr'\bshe {come_pattern}', message.lower()):
                send_message('she WHAT??')
            elif re.search(fr'\bhe {come_pattern}', message.lower()):
                send_message('he WHAT??')
            elif re.search(fr'\bthey {come_pattern}', message.lower()):
                send_message('they WHAT??')
            elif re.search(fr'\bit {come_pattern}', message.lower()):
                send_message('it WHAT??')
            elif re.search(fr"\b((i(['’]| a)m)|((you|we)('| a)re)) {come_pattern}", message.lower()):
                send_message("you're WHAT??")
            elif re.search(fr"\bshe(['’]| i)s {come_pattern}", message.lower()):
                send_message("she's WHAT??")
            elif re.search(fr"\bhe(['’]| i)s {come_pattern}", message.lower()):
                send_message("he's WHAT??")
            elif re.search(fr"\bit(['’]| i)s {come_pattern}", message.lower()):
                send_message("it's WHAT??")
            else:
                send_message(message[:come_result.start()].lower() + 'WHAT??')

    return '', HTTPStatus.NO_CONTENT


def send_move_chat_reminder() -> None:
    current_year = datetime.now().year
    send_message(f"well friends, tis the dawn of a new era. there's a new h-row on the block. if you haven't already, you might want to move me to the {current_year} h-row chat. check my help guide to see how to do that:\n\ngo.osu.edu/binghelp")


UNSOLICITED_MESSAGE_FUNCTIONS = {
    UnsolicitedMessage.ELON_MUSK: send_elon,
    UnsolicitedMessage.H: send_h,
    UnsolicitedMessage.HANNA_DRINK_WATER: send_drink_water,
    UnsolicitedMessage.HUMIDITY: send_air_piss,
    UnsolicitedMessage.MEME: send_normal_or_deep_fried_meme,
    UnsolicitedMessage.NOW_YOU_SEE_ME: send_now_you_see_me,
    UnsolicitedMessage.RAIN: send_sky_piss,
    UnsolicitedMessage.ROTATE_ALEX: send_alex,
    UnsolicitedMessage.THE_CAR_QUOTE: send_the_car_quote,
    UnsolicitedMessage.WAWA: send_call_wawa,
    UnsolicitedMessage.GO_OHIO: send_go_ohio,
    UnsolicitedMessage.BEATING_NEXT: send_beating_next,
    UnsolicitedMessage.HELLO: send_hello,
    UnsolicitedMessage.BING_10_PICKS: send_bing_10_picks,
    UnsolicitedMessage.MOVE_CHAT_REMINDER: send_move_chat_reminder
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
    

# sets time to send go ohio to 3 hours before kickoff and beat next 3 hours after kickoff
# triggered every Friday morning from August to January by cron-job.org
@app.route('/set-game-day-message-times', methods=['GET'])
def set_go_ohio():
    logging.info(f'Recieved request to set GO_OHIO, HELLO, and BEATING_NEXT date and time')
    set_game_day_messages_date_and_time()
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
