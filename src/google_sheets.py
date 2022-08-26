import os
import httplib2
from operator import itemgetter
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']


_discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
_sheets_service = build('sheets', 'v4', http=httplib2.Http(), discoveryServiceUrl=_discovery_url, developerKey=GOOGLE_API_KEY)


def get_range(range):
  result = _sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()['values']
  if len(result[0]) == 1:
    return list(map(lambda x : x[0], result))
  return result


def get_ranges(ranges):
  asdf = _sheets_service.spreadsheets().values().batchGet(spreadsheetId=SPREADSHEET_ID, ranges=ranges).execute()['valueRanges']
  return list(map(itemgetter('values'), asdf))


if __name__ == '__main__':
  print(get_ranges(['Settings!A2:A14']))
