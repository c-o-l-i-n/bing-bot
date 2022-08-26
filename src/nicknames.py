from google_sheets import get_range


NICKNAMES_GOOGLE_SHEET_RANGE = 'Nicknames!A2:B1000'


def get_nicknames():
	sheet_values = get_range(NICKNAMES_GOOGLE_SHEET_RANGE)

	nicknames = {}
	for row in sheet_values:
		nicknames[row[0]] = row[1]
	
	return nicknames


if __name__ == '__main__':
	print(get_nicknames())