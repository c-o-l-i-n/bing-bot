import os
import cfbd
from functools import cache
from zoneinfo import ZoneInfo
from datetime import datetime
from dateutil import parser
from randomize_unsolicited_message_times import CronJob, set_cron_job_date_and_time


COLLEGE_FOOTBALL_API_KEY = os.environ['COLLEGE_FOOTBALL_API_KEY']
PROXY_URL = os.environ['PROXY_URL']


# configure apis
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
  return next(filter(lambda c: c.name == conference_name, conferences_api.get_conferences())).abbreviation


@cache
def _get_conference_teams(conference_abbreviation: str) -> list[cfbd.Team]:
  return teams_api.get_teams(conference=conference_abbreviation)


@cache
def _get_mascot(team_name: str, conference_name: str) -> str:
  conference_abbreviation = _get_conference_abbreviation(conference_name)
  conference_teams =  _get_conference_teams(conference_abbreviation)
  return next(filter(lambda t: t.school == team_name, conference_teams)).mascot


def _get_next_game() -> cfbd.Game:
  now = datetime.now(tz=LOCAL_TZ)
  season = now.year if now.month > 1 else now.year - 1 # if January, use previous year as season
  games: list[cfbd.Game] = games_api.get_games(year=now.year, team='Ohio State')
  postseason_games: list[cfbd.Game] = games_api.get_games(year=season, team='Ohio State', season_type='postseason')
  games.extend(postseason_games)
  next_game = next(filter(lambda g: parser.parse(g.start_date).astimezone(LOCAL_TZ) > now, games))
  return next_game
  

def set_go_ohio_date_and_time() -> None:
  next_game = _get_next_game()
  start_datetime = parser.parse(next_game.start_date).astimezone(LOCAL_TZ)
  if next_game.start_time_tbd:
    start_datetime.hour = 12 # if game time TBD, assume noon game
  set_cron_job_date_and_time(CronJob.GO_OHIO, start_datetime.month, start_datetime.day, start_datetime.hour - 3, start_datetime.minute)


def send_go_ohio() -> None:
  next_game = _get_next_game()

  opponent_is_away_team: bool = next_game.away_team != 'Ohio State'
  opponent_name: str = next_game.away_team if opponent_is_away_team else next_game.home_team
  opponent_conference_name: str = next_game.away_conference if opponent_is_away_team else next_game.home_conference
  opponent_mascot: str = _get_mascot(opponent_name, opponent_conference_name)
  opponent_mascot_shortened: str = opponent_mascot[opponent_mascot.rindex(' ') + 1 :] if ' ' in opponent_mascot else opponent_mascot
  
  print(f'go ohio, beat the {opponent_mascot_shortened.lower()}!')


if __name__ == '__main__':
  send_go_ohio()
