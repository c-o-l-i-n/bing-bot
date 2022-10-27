import random
from college_football import get_next_game_opponent
from groupme_image_service import get_groupme_image_url_from_url
from send_message import send_message


GIFS = [
  'https://i.imgur.com/7IPkQZI.gif',
  'https://i.imgur.com/TogtoDx.gif',
  'https://i.imgur.com/X6PFVAl.gif',
  'https://i.imgur.com/MHX1Oej.gif',
  'https://i.imgur.com/5l6rAIL.gif',
  'https://i.imgur.com/2tj31JG.gif',
  'https://i.imgur.com/Kz59t3x.gif',
  'https://i.imgur.com/kEgg5eW.gif',
  'https://i.imgur.com/PCOovow.gif',
  'https://i.imgur.com/7wXCtwh.gif',
  'https://i.imgur.com/0ChkbHF.gif',
  'https://i.imgur.com/Z4UHd3e.gif',
  'https://i.imgur.com/U0aBJ4q.gif',
  'https://i.imgur.com/K49nmR5.gif',
  'https://i.imgur.com/ChBCfDt.gif',
  'https://i.imgur.com/UVXPVnb.gif',
  'https://i.imgur.com/lr0ioP7.gif',
  'https://i.imgur.com/HPCMqYV.gif',
  'https://i.imgur.com/zQ1yq58.gif',
  'https://i.imgur.com/il9Lw22.gif',
  'https://i.imgur.com/t3eoIHV.gif',
  'https://i.imgur.com/PKepqcf.gif'
]

TBDBITL_THROWING_M_IN_TRASH = 'https://i.imgur.com/uK6I9HB.gif'


def send_its_game_day() -> None:
  picture = random.choice(GIFS)
  
  opponent = get_next_game_opponent()
  if opponent == 'Michigan':
    picture = TBDBITL_THROWING_M_IN_TRASH

  send_message("it's game day", get_groupme_image_url_from_url(picture))


if __name__ == '__main__':
  send_its_game_day()
