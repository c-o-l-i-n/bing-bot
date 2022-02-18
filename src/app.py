import os
import requests
from flask import Flask, request, render_template
from send_message import send_message
from weather import get_weather, get_temperature
from custom_message_senders.send_the_car_quote import send_the_car_quote
from custom_message_senders.send_meme import send_meme


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

BING_SETTINGS_PASSWORD = os.environ['BING_SETTINGS_PASSWORD']

ALL_SETTINGS = [
    'are you alive',
    'hi bing',
    'i love you',
    'joke',
    'weather',
    'temperature',
    'make meme',
    'cook meal',
    'car quote',
    'good of the order',
    'one pizza pie',
    '69 420',
    'h ass ohio you suck',
    'cat call',
    'send "H" every day',
    'send a meme every day',
    'send a "Now You See Me" message every day',
    'remind Hanna to drink water every day',
    "send Jeff Bezos update every weekday",
    "send Elon Musk update every weekday",
    'check for rain every 30 minutes',
    'check for high humidity every 30 minutes',
    'ask if anyone called wawa every Saturday',
    'rotate Alex Gonzalez every day',
    'send a "Katie Paid" message every day',
    'send a quote from "The Car" every day'
]


# create flask instance
app = Flask(__name__)


@app.route('/bing', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data['text']
    sender_id = data['sender_id']
    settings = get_settings()

    if message_contains('bing', message):

        # says 'hi' back to sender, and includes name if they're in H-Row
        if settings['are you alive'] and message_contains('are you alive', message):
            send_message('yeah')

        # says 'hi' back to sender, and includes name if they're in H-Row
        if settings['hi bing'] and message_contains('hi bing', message) or message_contains('hi, bing', message):
            new_message = 'hi'
            if sender_id in SENDER_ID_TO_NAME.keys():
                new_message += f' {SENDER_ID_TO_NAME[sender_id]}'
            send_message(new_message)

        # says 'i love you' back to sender, and includes name if they're in H-Row
        if settings['i love you'] and message_contains('i love you', message):
            new_message = 'i love you too'
            if sender_id in SENDER_ID_TO_NAME.keys():
                new_message += f' {SENDER_ID_TO_NAME[sender_id]}'
            send_message(new_message)

        # tells a joke on demand
        if settings['joke'] and message_contains('joke', message):
            send_message(requests.get('https://icanhazdadjoke.com/',
                                      headers={'Accept': 'text/plain'}).text[:-1].lower())

        # gets weather on demand
        if settings['weather'] and message_contains('weather', message):
            send_message(get_weather())

        # gets temperature on demand
        if settings['temperature'] and message_contains('temperature', message):
            temperature = get_temperature()
            send_message(
                f'{temperature}{" (nice)" if "69" in temperature else ""}')

        # make a new meme on demand
        if settings['make meme'] and (message_contains('make', message) or message_contains('send', message)) and message_contains('meme', message):
            if sender_id in SENDER_ID_TO_NAME.keys():
                message_text = f'''ok {SENDER_ID_TO_NAME[data["sender_id"]]}, here's a new meme'''
            else:
                message_text = f'''ok, here's a new meme'''
            if message_contains('deep fried', message):
                send_meme(message_text=message_text, is_deep_fried=True)
            else:
                send_meme(message_text=message_text)

        # gives a random recipe
        if settings['cook meal'] and message_contains('cook', message) or message_contains('meal', message) or message_contains('dinner', message) or message_contains('lunch', message):
            recipe = requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php').json()
            send_message(f'you should have {recipe["meals"][0]["strMeal"].lower()}' + (("\n\n" + recipe['meals'][0]['strYoutube']) if recipe["meals"]
                                                                                       [0]["strYoutube"] else "") + (("\n\n" + recipe['meals'][0]['strSource']) if recipe["meals"][0]["strSource"] else ""))

        # sends a quote from the movie "The Car"
        if settings['car quote'] and message_contains('car', message) and (message_contains('line', message) or message_contains('quote', message)):
            send_the_car_quote()

    # has something for the good of the order
    if settings['good of the order'] and message_contains('good of the order', message):
        send_message('tits')

    # sings "One Pizza Pie"
    if settings['one pizza pie'] and 'one pizza pie' == message[-13:].lower() or 'one pizza pie' == message[-14:-1].lower() or '1 pizza pie' == message[-11:].lower() or '1 for me' == message[-12:-1].lower():
        send_message('🍕 one for me, 🍕 one for when i die')

    # sings "One Pizza Pie"
    if settings['one pizza pie'] and 'one for me' == message[-10:].lower() or 'one for me' == message[-11:-1].lower() or '1 for me' == message[-8:].lower() or '1 for me' == message[-9:-1].lower():
        send_message('🍕 one for when i die')

    # says "nice" when someone else says 69 or 420
    if settings['69 420'] and data['sender_type'] != 'bot' and (message_contains('69', message) or message_contains('420', message)):
        send_message('nice')

    # says "ass" after "h"
    if settings['h ass ohio you suck'] and data['sender_type'] != 'bot' and 'h' == message.lower():
        send_message('ass')

    # says "ohio" after "ass"
    if settings['are you alive'] and data['sender_type'] != 'bot' and 'ass' == message.lower():
        send_message('ohio')

    # says "you suck" after "ohio"
    if settings['h ass ohio you suck'] and data['sender_type'] != 'bot' and 'ohio' == message.lower():
        send_message('you suck!')

    # says "ohio, you suck" after "h, ass"
    if settings['h ass ohio you suck'] and data['sender_type'] != 'bot' and ('h ass' == message[-5:].lower() or 'h, ass' == message[-6:].lower()):
        send_message('ohio, you suck!')

    # says cat call if message sent by a woman in H-Row
    if settings['cat call'] and sender_id in WOMEN_SENDER_IDS:
        send_message(f'@{SENDER_ID_TO_NAME[sender_id]}', 'https://i.groupme.com/256x274.jpeg.ffbbd45a599d4756911bd92442a39440')

    return "ok", 200


def message_contains(substring, message_text):
    return substring.lower() in message_text.lower()


@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')


def get_settings():
    if not os.path.exists('settings.txt'):
        set_settings(ALL_SETTINGS)
    settings = {}
    with open('settings.txt') as settings_file:
        for line in settings_file:
            key = line[2:-1]
            value = line[0] == '*'
            settings[key] = value
    return settings


def set_settings(new_settings):
    with open('settings.txt', 'w+') as settings_file:
        for setting in ALL_SETTINGS:
            settings_file.write(f'{"*" if setting in new_settings else " "} {setting}\n')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('password.html')
    elif request.method == 'POST':
        if request.form['password'] != BING_SETTINGS_PASSWORD:
            return render_template('password.html', invalid_password=True)
        elif 'submission' in request.form.keys():
            new_settings = list(request.form.keys())
            new_settings.remove('password')
            new_settings.remove('submission')
            new_settings = [x.replace('-', ' ') for x in new_settings]
            set_settings(new_settings)
            return render_template('settings.html', settings=get_settings(), password=BING_SETTINGS_PASSWORD, settings_saved=True)
        return render_template('settings.html', settings=get_settings(), password=BING_SETTINGS_PASSWORD)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
