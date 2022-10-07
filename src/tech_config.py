import logging
from cachetools import cached, TTLCache
from google_sheets import get_range


TECH_CONFIG_RANGE = "'Tech Config'!B1:B4"


# cache tech config, ttl 10 minutes
@cached(TTLCache(maxsize=128, ttl=10 * 60))
def get_tech_config():
  logging.info('Getting tech config')
  tech_config = get_range(TECH_CONFIG_RANGE)
  logging.info(tech_config)
  return tech_config


def groupme_access_token():
  return get_tech_config()[0]


def groupme_bot_id():
  return get_tech_config()[1]


def weather_api_key():
  return get_tech_config()[2]


def imgflip_api_key():
  return get_tech_config()[3]

