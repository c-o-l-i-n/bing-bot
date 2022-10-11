import logging
import os
import cfbd
from functools import cache
from zoneinfo import ZoneInfo
from datetime import datetime
from dateutil import parser
from randomize_unsolicited_message_times import CronJob, set_cron_job_date_and_time
from send_message import send_message


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


def _get_next_game() -> cfbd.Game:
  logging.info('Getting next Ohio State game')
  now = datetime.now(tz=LOCAL_TZ)
  season = now.year if now.month > 1 else now.year - 1 # if January, use previous year as season
  logging.info(f'Getting games for the {season} season')
  games: list[cfbd.Game] = games_api.get_games(year=now.year, team='Ohio State')
  postseason_games: list[cfbd.Game] = games_api.get_games(year=season, team='Ohio State', season_type='postseason')
  games.extend(postseason_games)
  logging.info(f'Found {len(games)} games, including postseason')
  next_game = next(filter(lambda g: parser.parse(g.start_date).astimezone(LOCAL_TZ) > now, games))
  logging.info(f'Next game is {next_game.away_team} @ {next_game.home_team} on {next_game.start_date}{", start time TBD" if next_game.start_time_tbd else ""}')
  return next_game
  

def set_go_ohio_date_and_time() -> None:
  next_game = _get_next_game()
  start_datetime = parser.parse(next_game.start_date).astimezone(LOCAL_TZ)
  logging.info(f'The game is on {start_datetime.month}/{start_datetime.date}{"" if next_game.start_time_tbd else f" at {start_datetime.hour}:{start_datetime.minute:02d} {LOCAL_TZ} time"}')
  game_start_hour = start_datetime.hour
  if next_game.start_time_tbd:
    logging.info('Assuming noon game since time is TBD')
    game_start_hour = 12 # if game time TBD, assume noon game
  set_cron_job_date_and_time(CronJob.GO_OHIO, start_datetime.month, start_datetime.day, game_start_hour - 3, start_datetime.minute)


def send_go_ohio() -> None:
  next_game = _get_next_game()

  opponent_is_away_team: bool = next_game.away_team != 'Ohio State'
  opponent_name: str = next_game.away_team if opponent_is_away_team else next_game.home_team
  opponent_conference_name: str = next_game.away_conference if opponent_is_away_team else next_game.home_conference
  logging.info(f'Opponent is {opponent_name} ({"away" if opponent_is_away_team else "home"} team), {opponent_conference_name} conference')

  opponent_mascot: str = _get_mascot(opponent_name, opponent_conference_name)
  opponent_mascot_shortened: str = opponent_mascot[opponent_mascot.rindex(' ') + 1 :] if ' ' in opponent_mascot else opponent_mascot

  send_message(f'go ohio, beat the {opponent_mascot_shortened.lower()}!')


if __name__ == '__main__':
  send_go_ohio()
