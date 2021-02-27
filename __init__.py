import os
import json
import requests
from flask import Flask, request

from send_message import send_message
from send_meme import *
from weather import *


SENDER_ID_TO_NAME = {
    '41850231': 'tuggle',
    '39954190': 'mark',
    '51295820': 'buddy',
    '36464940': 'nic',
    '86238544': 'zach',
    '29486148': 'mc',
    '40390186': 'jay',
    '20322339': 'alayah',
    '18938463': 'toot',
    '86415518': 'ibby',
    '40404310': 'evan',
    '40438487': 'jacob',
    '60334407': 'andrew',
    '71705703': 'meetball man'
}

# create flask instance
app = Flask(__name__)
# app.config['DEBUG'] = True


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
                                      headers={'Accept': 'text/plain'}).text[:-1])

        # gets weather on demand
        if message_contains('weather', message):
            send_message(get_weather())

        # gets temperature on demand
        if message_contains('temperature', message):
            temperature = get_temperature()
            send_message(
                f'{temperature}{" (nice)" if "69" in temperature else ""}')

        # make a new meme on demand
        if message_contains('make', message) and message_contains('meme', message):
            send_meme(
                f'''ok {SENDER_ID_TO_NAME[data["sender_id"]]}, here's a new meme''')

        # gives a random recipe
        if message_contains('cook', message) or message_contains('meal', message) or message_contains('dinner', message) or message_contains('lunch', message):
            recipe = requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php').json()
            send_message(f'you should have {recipe["meals"][0]["strMeal"].lower()}' + (("\n\n" + recipe['meals'][0]['strYoutube']) if recipe["meals"]
                                                                                       [0]["strYoutube"] else "") + (("\n\n" + recipe['meals'][0]['strSource']) if recipe["meals"][0]["strSource"] else ""))

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

    return "ok", 200


def message_contains(substring, message_text):
    return substring.lower() in message_text.lower()


@app.route('/', methods=['GET'])
def get():
    return 'Hello from buddy-server!'


# run app
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=6969)
