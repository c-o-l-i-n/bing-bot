import logging
import os
import random
import cfbd
from functools import cache
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from dateutil import parser
from cron import CRON_JOB_TO_TIME_INTERVAL, CronJob, get_random_time_between, set_cron_job_date_and_time
from send_message import send_message
from time import sleep
from dotenv import load_dotenv


load_dotenv()
COLLEGE_FOOTBALL_API_KEY = os.environ['COLLEGE_FOOTBALL_API_KEY']
PROXY_URL = os.environ['PROXY_URL']


# configure apis
logging.info(f'Configuring College Football API with proxy {PROXY_URL}')
configuration = cfbd.Configuration()
configuration.proxy = PROXY_URL if PROXY_URL else None
configuration.api_key['Authorization'] = COLLEGE_FOOTBALL_API_KEY
configuration.api_key_prefix['Authorization'] = 'Bearer'
games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
conferences_api = cfbd.ConferencesApi(cfbd.ApiClient(configuration))
teams_api = cfbd.TeamsApi(cfbd.ApiClient(configuration))

LOCAL_TZ = ZoneInfo('US/Eastern')


@cache
def _get_conference_abbreviation(conference_name: str) -> str:
  logging.info(f'Getting abbreviation for {conference_name} conference')
  conference_abbreviation = next(filter(lambda c: c.name == conference_name, conferences_api.get_conferences())).abbreviation
  logging.info(f'Abbreviation for {conference_name} is {conference_abbreviation}')
  return conference_abbreviation


@cache
def _get_conference_teams(conference_abbreviation: str) -> list[cfbd.Team]:
  logging.info(f'Getting info for all teams in the {conference_abbreviation} conference')
  conference_teams: list[cfbd.Team] = teams_api.get_teams(conference=conference_abbreviation)
  logging.info(f'Found info for {len(conference_teams)} teams: {list(map(lambda t: t.abbreviation, conference_teams))}')
  return teams_api.get_teams(conference=conference_abbreviation)


@cache
def _get_mascot(team_name: str, conference_name: str) -> str:
  conference_abbreviation = _get_conference_abbreviation(conference_name)
  conference_teams =  _get_conference_teams(conference_abbreviation)
  logging.info(f'Getting mascot for {team_name}')
  mascot = next(filter(lambda t: t.school == team_name, conference_teams)).mascot
  logging.info(f'Mascot for {team_name} is the {mascot}')
  return mascot


def _get_current_season() -> int:
  now = datetime.now(tz=LOCAL_TZ)
  return now.year if now.month > 1 else now.year - 1 # if January, use previous year as season


def _get_next_game() -> cfbd.Game:
  logging.info('Getting next Ohio State game')
  now = datetime.now(tz=LOCAL_TZ)
  season = _get_current_season()
  logging.info(f'Getting games for the {season} season')
  games: list[cfbd.Game] = games_api.get_games(year=now.year, team='Ohio State')
  postseason_games: list[cfbd.Game] = games_api.get_games(year=season, team='Ohio State', season_type='postseason')
  games.extend(postseason_games)
  logging.info(f'Found {len(games)} games, including postseason')
  next_game = next(filter(lambda g: parser.parse(g.start_date).astimezone(LOCAL_TZ) > now, games), None)
  if not next_game:
    logging.info('No more games :(')
  else:
    logging.info(f'Next game is {next_game.away_team} @ {next_game.home_team} on {next_game.start_date}{", start time TBD" if next_game.start_time_tbd else ""}')
  return next_game


def send_bing_10_picks() -> None:
  # get all big 10 conference games for the next week
  season = _get_current_season()
  now = datetime.now(tz=LOCAL_TZ)
  a_week_from_now = now + timedelta(days=7)
  logging.info(f'Getting all games played by B1G teams in the {season} season')
  this_seasons_big_10_games: list[cfbd.Game] = games_api.get_games(year=season, conference='B1G')
  logging.info(f'Found {len(this_seasons_big_10_games)} games')
  logging.info(f'Getting all B1G conference games in the next week (between {now} and {a_week_from_now})')
  big_10_games_in_the_next_week: list[cfbd.Game] = list(filter(lambda g: parser.parse(g.start_date) > now and parser.parse(g.start_date) < a_week_from_now and g.conference_game, this_seasons_big_10_games))
  logging.info(f'Found {len(big_10_games_in_the_next_week)} games')
  
  if len(big_10_games_in_the_next_week) == 0:
    return
  
  #  get the current week number
  week = big_10_games_in_the_next_week[0].week
  logging.info(f'According to data from the {big_10_games_in_the_next_week[0].home_team} game, we are in week {week}')

  message = f"🦏🔟 picks for week {week}:\n\n"

  # move the ohio state game to the end of the list
  ohio_state_game = next(filter(lambda g: g.home_team == 'Ohio State' or g.away_team == 'Ohio State', big_10_games_in_the_next_week), None)
  if ohio_state_game:
    big_10_games_in_the_next_week.remove(ohio_state_game)
    big_10_games_in_the_next_week.append(ohio_state_game)

  # pick winning team for each game
  for game in big_10_games_in_the_next_week:
    winning_team, losing_team = (game.home_team, game.away_team) if game.home_pregame_elo > game.away_pregame_elo else (game.away_team, game.home_team)
    logging.info(f'{winning_team} is favored to beat {losing_team}')
    if random.random() < 0.2:
      logging.info(f'By random chance, swapping {losing_team} and {winning_team}')
      winning_team, losing_team = losing_team, winning_team
    if winning_team == 'Michigan':
      logging.info(f'Bing thinks TTUN will always lose because she hates them; swapping {losing_team} and {winning_team}')
      winning_team = losing_team
      losing_team = 'TTUN'
    if losing_team == 'Michigan':
      losing_team = 'TTUN'
    if losing_team == 'Ohio State':
      logging.info(f'Bing thinks Ohio State will always win; swapping {losing_team} and {winning_team}')
      losing_team = winning_team
      winning_team = 'Ohio State'
    
    emoji = '🏈'
    if losing_team == 'TTUN':
      emoji = '👺'
    elif winning_team == 'Ohio State':
      emoji = '🏆'

    message += f'{emoji} {winning_team} {"DESTROYS" if winning_team == "Ohio State" else "beats"} {losing_team}\n'

  send_message(message)


def set_game_day_messages_date_and_time() -> None:
  next_game = _get_next_game()
  if not next_game:
    return
  start_datetime = parser.parse(next_game.start_date).astimezone(LOCAL_TZ)
  logging.info(f'The game is on {start_datetime.month}/{start_datetime.day}{"" if next_game.start_time_tbd else f" at {start_datetime.hour}:{start_datetime.minute:02d} {LOCAL_TZ} time"}')
  if next_game.start_time_tbd:
    logging.info('Assuming noon game since time is TBD')
    start_datetime.hour = 12
  
  # WAWA
  wawa_min_hour, wawa_max_hour = CRON_JOB_TO_TIME_INTERVAL[CronJob.WAWA]
  wawa_hour, wawa_minute = get_random_time_between(wawa_min_hour, wawa_max_hour)
  set_cron_job_date_and_time(CronJob.WAWA, start_datetime.month, start_datetime.day, wawa_hour, wawa_minute)
  sleep(0.5) # avoid API usage limit

  # ITS_GAME_DAY
  its_game_day_time = start_datetime - timedelta(hours=6, minutes=30)
  set_cron_job_date_and_time(CronJob.ITS_GAME_DAY, start_datetime.month, start_datetime.day, its_game_day_time.hour, its_game_day_time.minute)
  sleep(0.5) # avoid API usage limit

  # GO_OHIO
  set_cron_job_date_and_time(CronJob.GO_OHIO, start_datetime.month, start_datetime.day, start_datetime.hour - 3, start_datetime.minute)
  sleep(0.5) # avoid API usage limit
  
  # HELLO
  its_game_day_time = start_datetime - timedelta(minutes=30)
  set_cron_job_date_and_time(CronJob.HELLO, start_datetime.month, start_datetime.day, its_game_day_time.hour, its_game_day_time.minute)
  sleep(0.5) # avoid API usage limit
  
  # BEATING_NEXT
  set_cron_job_date_and_time(CronJob.BEATING_NEXT, start_datetime.month, start_datetime.day, start_datetime.hour + 3, start_datetime.minute)


def _get_next_game_opponent_mascot() -> str:
  next_game = _get_next_game()

  if not next_game:
    return None

  opponent_is_away_team: bool = next_game.away_team != 'Ohio State'
  opponent_name: str = next_game.away_team if opponent_is_away_team else next_game.home_team

  if opponent_name == 'Michigan':
    return 'm*chigan'

  opponent_conference_name: str = next_game.away_conference if opponent_is_away_team else next_game.home_conference
  logging.info(f'Opponent is {opponent_name} ({"away" if opponent_is_away_team else "home"} team), {opponent_conference_name} conference')

  opponent_mascot: str = _get_mascot(opponent_name, opponent_conference_name)
  opponent_mascot_shortened: str = opponent_mascot[opponent_mascot.rindex(' ') + 1 :] if ' ' in opponent_mascot else opponent_mascot

  return f'the {opponent_mascot_shortened.lower()}'


def send_go_ohio() -> None:
  mascot = _get_next_game_opponent_mascot()
  if not mascot:
    return
  send_message(f'go ohio, beat {mascot}!')


def send_beating_next() -> None:
  mascot = _get_next_game_opponent_mascot()
  if not mascot:
    return
  send_message(f'(beating {mascot} next)')


def next_game_is_home_game() -> bool:
  next_game = _get_next_game()
  return next_game.home_team == 'Ohio State'


def get_next_game_opponent() -> str:
  next_game = _get_next_game()
  return next_game.home_team if next_game.away_team == 'Ohio State' else next_game.away_team


if __name__ == '__main__':
  send_go_ohio()
  send_bing_10_picks()
  send_beating_next()
