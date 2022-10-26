import random
from college_football import get_next_game_opponent
from groupme_image_service import get_groupme_image_url_from_url
from send_message import send_message


PICTURES = [
  'https://i.imgur.com/mnvuXAw.jpg',
  'https://i.imgur.com/XhlkV5A.jpg',
  'https://i.imgur.com/xRDfG0L.jpg',
  'https://i.imgur.com/7IPkQZI.gif',
  'https://i.imgur.com/XWx9bYa.jpg',
  'https://i.imgur.com/GNZTYAP.jpg',
  'https://i.imgur.com/kRPkiJr.jpg',
  'https://i.imgur.com/3VawzwL.png',
  'https://i.imgur.com/HLHuo9I.jpg',
  'https://i.imgur.com/KxkXgHO.jpg',
  'https://i.imgur.com/z9xCDFE.jpg',
  'https://i.imgur.com/RVcCrgY.png',
  'https://i.imgur.com/WVx3wMm.jpg',
  'https://i.imgur.com/oSw8Sns.jpg',
  'https://i.imgur.com/nlU2Tvo.jpg',
  'https://i.imgur.com/FKGTggz.jpg'
]

BRUTUS_BEATING_WOLVERINE = 'https://i.imgur.com/6Z3UxyI.jpg'

BRUTUS_BEHIND_SPARTY = 'https://i.imgur.com/0wkQM3p.jpg'

def send_its_game_day():
  picture = random.choice(PICTURES)
  
  opponent = get_next_game_opponent()
  if opponent == 'Michigan':
    picture = BRUTUS_BEATING_WOLVERINE
  elif opponent == 'Michigan State':
    picture = BRUTUS_BEHIND_SPARTY

  send_message("it's game day", get_groupme_image_url_from_url(picture))


if __name__ == '__main__':
  send_its_game_day()
