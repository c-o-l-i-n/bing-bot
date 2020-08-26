import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

from groupme_bot_id import GROUPME_BOT_ID


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/bing', methods=['POST'])
def webhook():
    data = request.get_json()

    # We don't want to reply to ourselves!
    if data['sender_id'].lower() != '841754':
        msg = '{}, you sent {}.'.format(data['name'], data['text'])
        send_message(msg)

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