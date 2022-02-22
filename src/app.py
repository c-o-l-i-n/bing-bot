import os
import logging
import requests
from flask import Flask, request, render_template
from models import db, Setting, GroupmeUser
from send_message import send_message
from weather import get_weather, get_temperature
from custom_message_senders.send_the_car_quote import send_the_car_quote
from custom_message_senders.send_meme import send_meme


# set logging config
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


# initialize Flask app
logging.info('Creating Flask app')
app = Flask(__name__)
logging.info('Setting Flask app config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize database
logging.info('Initializing app for use with database')
app.app_context().push()
db.init_app(app)


@app.before_first_request
def before_first_request():
    # get nicknames of groupme users
    logging.info('Getting GroupMe users from database')
    global GROUPME_USER_ID_TO_NAME
    GROUPME_USER_ID_TO_NAME = {}
    try:
        all_groupme_users = GroupmeUser.query.all()
        for groupme_user in all_groupme_users:
            GROUPME_USER_ID_TO_NAME[str(groupme_user.id)] = groupme_user.nickname
        logging.info(f'GROUPME_USER_ID_TO_NAME: {GROUPME_USER_ID_TO_NAME}')
    except Exception as exception:
        logging.error(exception)

    # get women users
    logging.info('Getting women users')
    global WOMEN_GROUPME_USER_IDS
    WOMEN_GROUPME_USER_IDS = [x.id for x in all_groupme_users if x.is_woman]
    logging.info(f'WOMEN_GROUPME_USER_IDS: {WOMEN_GROUPME_USER_IDS}')

    # get bing settings password
    logging.info('Getting settings password')
    global BING_SETTINGS_PASSWORD
    BING_SETTINGS_PASSWORD = os.environ['BING_SETTINGS_PASSWORD']


@app.route('/bing', methods=['POST'])
def receive_message():
    logging.info(f'Message received')

    # get message data
    data = request.get_json()
    message = data['text']
    name = data['name']
    sender_id = data['sender_id']
    sender_type = data['sender_type']

    if sender_type != 'user':
        logging.info(f'From {sender_type}')
        return "ok", 200
    
    logging.info(f'From {name} ({sender_id}): {message}')

    settings = get_settings()
    logging.info(settings)

    if message_contains('bing', message):

        # says 'hi' back to sender, and includes name if they're in H-Row
        if setting_is_turned_on('are you alive', settings) and message_contains('are you alive', message):
            send_message('yeah')

        # says 'hi' back to sender, and includes name if they're in H-Row
        if setting_is_turned_on('hi bing', settings) and (message_contains('hi bing', message) or message_contains('hi, bing', message)):
            new_message = 'hi'
            if sender_id in GROUPME_USER_ID_TO_NAME.keys():
                new_message += f' {GROUPME_USER_ID_TO_NAME[sender_id]}'
            send_message(new_message)

        # says 'i love you' back to sender, and includes name if they're in H-Row
        if setting_is_turned_on('i love you', settings) and message_contains('i love you', message):
            new_message = 'i love you too'
            if sender_id in GROUPME_USER_ID_TO_NAME.keys():
                new_message += f' {GROUPME_USER_ID_TO_NAME[sender_id]}'
            send_message(new_message)

        # tells a joke on demand
        if setting_is_turned_on('joke', settings) and message_contains('joke', message):
            send_message(requests.get('https://icanhazdadjoke.com/',
                                      headers={'Accept': 'text/plain'}).text[:-1].lower())

        # gets weather on demand
        if setting_is_turned_on('weather', settings) and message_contains('weather', message):
            send_message(get_weather())

        # gets temperature on demand
        if setting_is_turned_on('temperature', settings) and message_contains('temperature', message):
            temperature = get_temperature()
            send_message(
                f'{temperature}{" (nice)" if "69" in temperature else ""}')

        # make a new meme on demand
        if setting_is_turned_on('make meme', settings) and ((message_contains('make', message) or message_contains('send', message)) and message_contains('meme', message)):
            if sender_id in GROUPME_USER_ID_TO_NAME.keys():
                message_text = f'''ok {GROUPME_USER_ID_TO_NAME[data["sender_id"]]}, here's a new meme'''
            else:
                message_text = f'''ok, here's a new meme'''
            if message_contains('deep fried', message):
                send_meme(message_text=message_text, is_deep_fried=True)
            else:
                send_meme(message_text=message_text)

        # gives a random recipe
        if setting_is_turned_on('cook meal', settings) and (message_contains('cook', message) or message_contains('meal', message) or message_contains('dinner', message) or message_contains('lunch', message)):
            recipe = requests.get(
                'https://www.themealdb.com/api/json/v1/1/random.php').json()
            send_message(f'you should have {recipe["meals"][0]["strMeal"].lower()}' + (("\n\n" + recipe['meals'][0]['strYoutube']) if recipe["meals"]
                                                                                       [0]["strYoutube"] else "") + (("\n\n" + recipe['meals'][0]['strSource']) if recipe["meals"][0]["strSource"] else ""))

        # sends a quote from the movie "The Car"
        if setting_is_turned_on('car quote', settings) and (message_contains('car', message) and (message_contains('line', message) or message_contains('quote', message))):
            send_the_car_quote()

    # has something for the good of the order
    if setting_is_turned_on('good of the order', settings) and message_contains('good of the order', message):
        send_message('tits')

    # sings "One Pizza Pie"
    if setting_is_turned_on('one pizza pie', settings) and ('one pizza pie' == message[-13:].lower() or 'one pizza pie' == message[-14:-1].lower() or '1 pizza pie' == message[-11:].lower() or '1 for me' == message[-12:-1].lower()):
        send_message('🍕 one for me, 🍕 one for when i die')

    # sings "One Pizza Pie"
    if setting_is_turned_on('one pizza pie', settings) and ('one for me' == message[-10:].lower() or 'one for me' == message[-11:-1].lower() or '1 for me' == message[-8:].lower() or '1 for me' == message[-9:-1].lower()):
        send_message('🍕 one for when i die')

    # says "nice" when someone else says 69 or 420
    if setting_is_turned_on('69 420', settings) and data['sender_type'] != 'bot' and ((message_contains('69', message) or message_contains('420', message))):
        send_message('nice')

    # says "ass" after "h"
    if setting_is_turned_on('h ass ohio you suck', settings) and data['sender_type'] != 'bot' and 'h' == message.lower():
        send_message('ass')

    # says "ohio" after "ass"
    if setting_is_turned_on('are you alive', settings) and data['sender_type'] != 'bot' and 'ass' == message.lower():
        send_message('ohio')

    # says "you suck" after "ohio"
    if setting_is_turned_on('h ass ohio you suck', settings) and data['sender_type'] != 'bot' and 'ohio' == message.lower():
        send_message('you suck!')

    # says "ohio, you suck" after "h, ass"
    if setting_is_turned_on('h ass ohio you suck', settings) and (data['sender_type'] != 'bot' and ('h ass' == message[-5:].lower() or 'h, ass' == message[-6:].lower())):
        send_message('ohio, you suck!')

    # says cat call if message sent by a woman in H-Row
    if setting_is_turned_on('cat call', settings) and sender_id in WOMEN_GROUPME_USER_IDS:
        send_message(f'@{GROUPME_USER_ID_TO_NAME[sender_id]}', 'https://i.groupme.com/256x274.jpeg.ffbbd45a599d4756911bd92442a39440')

    return "ok", 200


def message_contains(substring, message_text):
    return substring.lower() in message_text.lower()


@app.route('/', methods=['GET'])
def get():
    logging.info(f'Serving index page')
    return render_template('index.html')


def get_settings():
    logging.info('Getting settings from database')
    try:
        return Setting.query.all()
    except Exception as exception:
        logging.error(exception)
        return {}


def set_settings(new_settings):
    logging.info(f'Setting new settings: {new_settings}')
    try:
        for setting in Setting.query.all():
            setting.value = setting.name in new_settings
        db.session.commit()
        return True
    except Exception as exception:
        logging.error(exception)
        return False


def setting_is_turned_on(setting, settings):
    try:
        return next(filter(lambda x: x.name == setting, settings), None).value
    except Exception as exception:
        logging.error(exception)
        return False


def render_settings_page(is_updating_settings=False, updated_successfully=False):
    settings = get_settings()
    logging.info(settings)

    command_settings = [setting for setting in sorted(settings, key=lambda x: x.category_position) if setting.category == 'command']
    scheduled_settings = [setting for setting in sorted(settings, key=lambda x: x.category_position) if setting.category == 'scheduled']
    
    logging.info('Serving settings page')
    return render_template('settings.html', command_settings=command_settings, scheduled_settings=scheduled_settings, password=BING_SETTINGS_PASSWORD, is_updating_settings=is_updating_settings, updated_successfully=updated_successfully)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        # go to password input screen
        logging.info(f'Serving settings password page')
        return render_template('password.html')
    
    if request.method == 'POST':
        if request.form['password'] != BING_SETTINGS_PASSWORD:
            # invalib password; reload password input screen
            logging.info(f"User input invalid password: \"{request.form['password']}\"")
            logging.info(f'Re-serving settings password page')
            return render_template('password.html', invalid_password=True)
        
        if 'submission' in request.form.keys():
            # user submitted new settings
            # set new settings
            logging.info(f"User submitted new settings")
            new_settings = list(request.form.keys())
            new_settings.remove('password')
            new_settings.remove('submission')
            new_settings = [x.replace('-', ' ') for x in new_settings]
            successful = set_settings(new_settings)

            # reload settings page with updated settings
            return render_settings_page(is_updating_settings=True, updated_successfully=successful)
        
        # user typed password correctly
        # load settings page
        logging.info(f'User typed password correctly')
        return render_settings_page()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
