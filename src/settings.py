from enum import Enum, auto
import logging
from typing import Union
from google_sheets import get_ranges


class Command(Enum):
	ARE_YOU_ALIVE = auto()
	HELP = auto()
	HI = auto()
	I_LOVE_YOU = auto()
	JOKE = auto()
	WEATHER = auto()
	TEMPERATURE = auto()
	MAKE_MEME = auto()
	COOK_MEAL = auto()
	THE_CAR_QUOTE = auto()
	GOOD_OF_THE_ORDER = auto()
	ONE_PIZZA_PIE = auto()
	FUNNY_NUMBERS = auto()
	HAOUS = auto()
	BORED = auto()
	WHAT_IS_THIS = auto()
	DOG = auto()
	CAT = auto()
	COME = auto()
	DRAW = auto()

class UnsolicitedMessage(Enum):
	H = 'h'
	MEME = 'meme'
	NOW_YOU_SEE_ME = 'now-you-see-me'
	HANNA_DRINK_WATER = 'hanna-drink-water'
	ELON_MUSK = 'elon-musk'
	RAIN = 'rain'
	HUMIDITY = 'humidity'
	WAWA = 'wawa'
	ROTATE_ALEX = 'rotate-alex'
	THE_CAR_QUOTE = 'the-car-quote'
	GO_OHIO = 'go-ohio'
	BEATING_NEXT = 'beating-next'
	HELLO = 'hello'
	ITS_GAME_DAY = 'its-game-day'
	BING_10_PICKS = 'bing-10-picks'
	MOVE_CHAT_REMINDER = 'move-chat-reminder'


SETTINGS_ROW_OFFSET = 2
SETTINGS_GOOGLE_SHEET_RANGES = [
	f'Settings!A{SETTINGS_ROW_OFFSET + 1}:A{len(Command) + SETTINGS_ROW_OFFSET}',
	f'Settings!D{SETTINGS_ROW_OFFSET + 1}:D{len(UnsolicitedMessage) + SETTINGS_ROW_OFFSET}'
]


def _convert_ranges_to_booleans(value_ranges: list[list[list[str]]]) -> list[list[bool]]:
	rt: list[list[bool]] = []

	for i, category in enumerate(value_ranges):
		rt.append([])
		for setting in category:
			rt[i].append(setting == ['TRUE'])

	return rt


def get_settings() -> dict[Union[Command, UnsolicitedMessage], bool]:
	logging.info('Getting settings from Google Sheet')
	settings: dict[Union[Command, UnsolicitedMessage], bool] = {}
	command_settings_values, unsolicited_message_settings_values = _convert_ranges_to_booleans(get_ranges(SETTINGS_GOOGLE_SHEET_RANGES))
	
	for i, command_setting in enumerate(Command):
		settings[command_setting] = command_settings_values[i]
	
	for i, unsolicited_message_setting in enumerate(UnsolicitedMessage):
		settings[unsolicited_message_setting] = unsolicited_message_settings_values[i]
	
	logging.info(settings)
	return settings


if __name__ == '__main__':
	print(get_settings())
