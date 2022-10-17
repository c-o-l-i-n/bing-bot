import json
import logging
import os
import time
import websocket
from dotenv import load_dotenv

load_dotenv()
COLLEGE_FOOTBALL_API_KEY = os.environ['COLLEGE_FOOTBALL_API_KEY']
PROXY_HOST = os.environ['PROXY_HOST']
PROXY_PORT = os.environ['PROXY_PORT']

prompt = ''
image_data_uri = ''

def on_message(ws: websocket.WebSocketApp, message_bytes):
    message = json.loads(message_bytes)

    global image_data_uri

    if 'msg' in message:
        logging.info(message['msg'])
        if message['msg'] == 'process_completed':
            image_data_uri = message['output']['data'][0][0]
            ws.close()
    else:
        logging.info(message)


def on_error(ws: websocket.WebSocketApp, error):
    logging.info(f'ERROR: {error}')


def on_close(ws: websocket.WebSocketApp, close_status_code, close_msg):
    logging.info("### closed ###")
    logging.info(f'{close_status_code}: {close_msg}')


def on_open(ws: websocket.WebSocketApp):
    global image_data_uri
    global prompt
    image_data_uri = ''
    logging.info("Opened connection")
    logging.info('sending prompt data')
    ws.send(json.dumps({
        'fn_index': 2,
        'data': [prompt],
        'session_hash': 'bingbot1416'
    }))


def draw(ai_prompt: str) -> str:
    global image_data_uri
    global prompt

    image_data_uri = ''
    prompt = ai_prompt

    try_count = 0
    max_num_tries = 5
    seconds_between_tries = 2

    websocket.enableTrace(True)

    while try_count < max_num_tries:
        ws = websocket.WebSocketApp('wss://spaces.huggingface.tech/stabilityai/stable-diffusion/queue/join',
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

        if PROXY_HOST:
            ws.run_forever(proxy_type='http', http_proxy_host=PROXY_HOST, http_proxy_port=PROXY_PORT)
        else:
            ws.run_forever()

        if image_data_uri != '':
            break

        time.sleep(seconds_between_tries)
        try_count += 1


    return image_data_uri


if __name__ == "__main__":
    draw()
