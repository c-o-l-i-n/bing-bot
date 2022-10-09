import os
import json
import requests
import random
from time import sleep
from typing import Tuple
from enum import Enum
from http import HTTPStatus


CRON_JOB_ORG_API_KEY = os.environ['CRON_JOB_ORG_API_KEY']


class CronJob(Enum):
  ELON_MUSK = 4065111
  H = 4065114
  HANNA_DRINK_WATER = 4065135
  MEME = 4065131
  NOW_YOU_SEE_ME = 4065133
  ROTATE_ALEX = 4065141
  THE_CAR_QUOTE = 4065143
  WAWA = 4065140


CRON_JOB_TO_TIME_INTERVAL: dict[CronJob, Tuple[int, int]] = {
  CronJob.ELON_MUSK: (17, 20),
  CronJob.H: (9, 22),
  CronJob.HANNA_DRINK_WATER: (9, 22),
  CronJob.MEME: (9, 22),
  CronJob.NOW_YOU_SEE_ME: (9, 22),
  CronJob.ROTATE_ALEX: (9, 22),
  CronJob.THE_CAR_QUOTE: (9, 22),
  CronJob.WAWA: (3, 6),
}


def set_cron_job_time(cron_job: CronJob, hour: int, minute: int) -> None:
  print(f'Setting cron job {cron_job.name} ({cron_job.value}) time to {hour}:{minute:02d}', flush=True)

  ENDPOINT = f'https://api.cron-job.org/jobs/{cron_job.value}'
  headers = {
    'Authorization': f'Bearer {CRON_JOB_ORG_API_KEY}',
    'Content-Type': 'application/json'
  }
  payload = {
    'job': {
      'schedule': {
        'hours': [hour],
        'minutes': [minute]
      }
    }
  }

  response = requests.patch(ENDPOINT, headers=headers, data=json.dumps(payload))
  
  if response.status_code == HTTPStatus.OK:
    print(f'Success', flush=True)
  else:
    print(f'Failed :( {response.status_code} {response.text}', flush=True)


def _get_random_time_between(start_hour: int, end_hour: int) -> Tuple[int, int]:
  hour = random.randrange(start_hour, end_hour)
  minute = random.randrange(60)
  return (hour, minute)


def randomize_unsolicited_message_times() -> None:
  for cron_job in CRON_JOB_TO_TIME_INTERVAL:
    start_hour, end_hour = CRON_JOB_TO_TIME_INTERVAL[cron_job]
    hour, minute = _get_random_time_between(start_hour, end_hour)
    set_cron_job_time(cron_job, hour, minute)
    sleep(1) # avoid API usage limit


# to be run once daily before cron jobs begin
if __name__ == '__main__':
  randomize_unsolicited_message_times()
