import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

from groupme_bot_id import GROUPME_BOT_ID


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
def webhook():
    data = request.get_json()

    # says 'hi' back to sender, and includes name if they're in H-Row
    if 'hi bing' in data['text'].lower() or 'hi, bing' in data['text'].lower():
        message = 'hi'
        if data['sender_id'] in SENDER_ID_TO_NAME.keys():
            message += f' {SENDER_ID_TO_NAME[data["sender_id"]]}'
        send_message(message)

    # has something for the good of the order
    if 'good of the order' in data['text'].lower():
        send_message('tits')

    return "ok", 200


@app.route('/', methods=['GET'])
def get():
    return 'Hello from buddy-server!'


def send_message(msg):
    url  = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id' : GROUPME_BOT_ID,
        'text'   : msg,
    }

    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()


# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
