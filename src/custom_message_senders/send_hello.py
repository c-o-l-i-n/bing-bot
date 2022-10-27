import logging
from college_football import next_game_is_home_game
from send_message import send_message


def send_hello() -> None:
  if not next_game_is_home_game(): 
    logging.info('This game is not a home game, so not sending HELLO message')
    return
  
  send_message('👋 HELLOOOOOOOO')


if __name__ == '__main__':
  send_hello()
