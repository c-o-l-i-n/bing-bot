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
app.config['DEBUG'] = True


@app.route('/bing', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data['text']
    sender_id = data['sender_id']

    # says 'hi' back to sender, and includes name if they're in H-Row
    if messaage_contains('hi bing', message) or messaage_contains('hi, bing', message):
        new_message = 'hi'
        if sender_id in SENDER_ID_TO_NAME.keys():
            new_message += f' {SENDER_ID_TO_NAME[sender_id]}'
        send_message(new_message)

    # says 'i love you' back to sender, and includes name if they're in H-Row
    if messaage_contains('i love you', message) and messaage_contains('bing', message):
        new_message = 'i love you too'
        if sender_id in SENDER_ID_TO_NAME.keys():
            new_message += f' {SENDER_ID_TO_NAME[sender_id]}'
        send_message(new_message)

    # has something for the good of the order
    if messaage_contains('good of the order', message):
        send_message('tits')

    # tells a joke on demand
    if messaage_contains('joke', message) and messaage_contains('bing', message):
        send_message(requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'text/plain'}).text[:-1])

    # gets weather on demand
    if messaage_contains('weather', message) and messaage_contains('bing', message):
        send_message(get_weather())

    # gets temperature on demand
    if messaage_contains('temperature', message) and messaage_contains('bing', message):
        send_message(get_temperature())

    # make a new meme on demand
    if messaage_contains('make', message) and messaage_contains('meme', message) and messaage_contains('bing', message):
        send_meme(f'''ok {SENDER_ID_TO_NAME[data["sender_id"]]}, here's a new meme''')

    return "ok", 200


def messaage_contains(substring, message_text):
    return substring.lower() in message_text.lower()


@app.route('/', methods=['GET'])
def get():
    return 'Hello from buddy-server!'


# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
