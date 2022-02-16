import os
import json
import requests
from flask import Flask, request
from send_message import send_message
from send_meme import *
from weather import *
from send_the_car_quote import send_the_car_quote


SENDER_ID_TO_NAME = {
    '41850231': 'taco',
    '39954190': 'bloon hands',
    '51295820': 'buddy',
    '36464940': 'gneurshk',
    '86238544': 'flerken',
    '29486148': 'mc',
    '40390186': 'flame',
    '20322339': 'jorgen',
    '18938463': 'toot',
    '40438487': 'falco',
    '60334407': 'jasper',
    '71705703': 'meetball',
    '21493055': 'moon shoes',
    '36684822': 'brick'
}

WOMEN_SENDER_IDS = ['29486148', '20322339', '18938463']


# create flask instance
app = Flask(__name__)


@app.route('/bing', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data['text']
    sender_id = data['sender_id']

    if message_contains('bing', message):

        # says 'hi' back to sender, and includes name if they're in H-Row
        if message_contains('are you alive', message):
            send_message('yeah')

        # says 'hi' back to sender, and includes name if they're in H-Row
        if message_contains('hi bing', message) or message_contains('hi, bing', message):
            new_message = 'hi'
            if sender_id in SENDER_ID_TO_NAME.keys():
                new_message += f' {SENDER_ID_TO_NAME[sender_id]}'
            send_message(new_message)

        # says 'i love you' back to sender, and includes name if they're in H-Row
        if message_contains('i love you', message):
            new_message = 'i love you too'
            if sender_id in SENDER_ID_TO_NAME.keys():
                new_message += f' {SENDER_ID_TO_NAME[sender_id]}'
            send_message(new_message)

        # tells a joke on demand
        if message_contains('joke', message):
            send_message(requests.get('https://icanhazdadjoke.com/',
                                      headers={'Accept': 'text/plain'}).text[:-1].lower())

        # gets weather on demand
        if message_contains('weather', message):
            send_message(get_weather())

        # gets temperature on demand
        if message_contains('temperature', message):
            temperature = get_temperature()
            send_message(
                f'{temperature}{" (nice)" if "69" in temperature else ""}')

        # make a new meme on demand
        if (message_contains('make', message) or message_contains('send', message)) and message_contains('meme', message):
            if sender_id in SENDER_ID_TO_NAME.keys():
                message_text = f'''ok {SENDER_ID_TO_NAME[data["sender_id"]]}, here's a new meme'''
            else:
                message_text = f'''ok, here's a new meme'''
            if message_contains('deep fried', message):
                send_meme(message_text=message_text, is_deep_fried=True)
            else:
                send_meme(message_text=message_text)

        # gives a random recipe
        if message_contains('cook', message) or message_contains('meal', message) or message_contains('dinner', message) or message_contains('lunch', message):
            recipe = requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php').json()
            send_message(f'you should have {recipe["meals"][0]["strMeal"].lower()}' + (("\n\n" + recipe['meals'][0]['strYoutube']) if recipe["meals"]
                                                                                       [0]["strYoutube"] else "") + (("\n\n" + recipe['meals'][0]['strSource']) if recipe["meals"][0]["strSource"] else ""))

        # sends a quote from the movie "The Car"
        if message_contains('car', message) and (message_contains('line', message) or message_contains('quote', message)):
            send_the_car_quote()

    # has something for the good of the order
    if message_contains('good of the order', message):
        send_message('tits')

    # sings "One Pizza Pie"
    if 'one pizza pie' == message[-13:].lower() or 'one pizza pie' == message[-14:-1].lower() or '1 pizza pie' == message[-11:].lower() or '1 for me' == message[-12:-1].lower():
        send_message('🍕 one for me, 🍕 one for when i die')

    # sings "One Pizza Pie"
    if 'one for me' == message[-10:].lower() or 'one for me' == message[-11:-1].lower() or '1 for me' == message[-8:].lower() or '1 for me' == message[-9:-1].lower():
        send_message('🍕 one for when i die')

    # says "nice" when someone else says 69 or 420
    if data['sender_type'] != 'bot' and (message_contains('69', message) or message_contains('420', message)):
        send_message('nice')

    # says "ass" after "h"
    if data['sender_type'] != 'bot' and 'h' == message.lower():
        send_message('ass')

    # says "ohio" after "ass"
    if data['sender_type'] != 'bot' and 'ass' == message.lower():
        send_message('ohio')

    # says "you suck" after "ohio"
    if data['sender_type'] != 'bot' and 'ohio' == message.lower():
        send_message('you suck!')

    # says "ohio, you suck" after "h, ass"
    if data['sender_type'] != 'bot' and ('h ass' == message[-5:].lower() or 'h, ass' == message[-6:].lower()):
        send_message('ohio, you suck!')

    # says cat call if message sent by a woman in H-Row
    if sender_id in WOMEN_SENDER_IDS:
        send_message(f'@{SENDER_ID_TO_NAME[sender_id]}', 'https://i.groupme.com/256x274.jpeg.ffbbd45a599d4756911bd92442a39440')

    return "ok", 200


def message_contains(substring, message_text):
    return substring.lower() in message_text.lower()


@app.route('/', methods=['GET'])
def get():
    return "Hello from Bing's server!"


if __name__ == '__main__':
    app.run()