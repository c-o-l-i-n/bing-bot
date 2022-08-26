import logging
from google_sheets import get_range, set_range


SHEET_NAME = 'Nicknames'
ID_COLUMN = 'A'
NICKNAME_COLUMN = 'B'
NICKNAMES_GOOGLE_SHEET_RANGE = f'{SHEET_NAME}!{ID_COLUMN}2:{NICKNAME_COLUMN}1000'


def get_nicknames():
	logging.info(f'Getting nicknames from Google Sheet')
	sheet_values = get_range(NICKNAMES_GOOGLE_SHEET_RANGE)

	nicknames = {}
	for row in sheet_values:
		nicknames[row[0]] = row[1]
	
	return nicknames


def create_new_nickname(id, nickname):
	nicknames = get_nicknames()
	row = len(nicknames) + 2
	range = f'{SHEET_NAME}!{ID_COLUMN}{row}:{NICKNAME_COLUMN}{row}'
	logging.info(f'Adding nickname {id}: {nickname} to range {range}')
	set_range(range, [id, nickname])


if __name__ == '__main__':
	print(get_nicknames())
