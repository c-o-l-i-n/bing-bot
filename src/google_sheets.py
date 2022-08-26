import logging
import os
from operator import itemgetter
from dotenv import load_dotenv
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build


load_dotenv()
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

_creds = GoogleCredentials.get_application_default().create_scoped(['https://www.googleapis.com/auth/spreadsheets'])
_sheets_service = build('sheets', 'v4', credentials=_creds)


def get_range(range):
  logging.info(f'Getting Google Sheet range {range}')
  result = _sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()['values']
  if len(result[0]) == 1:
    return list(map(lambda x : x[0], result))
  return result


def get_ranges(ranges):
  logging.info(f'Getting Google Sheet ranges {ranges}')
  asdf = _sheets_service.spreadsheets().values().batchGet(spreadsheetId=SPREADSHEET_ID, ranges=ranges).execute()['valueRanges']
  return list(map(itemgetter('values'), asdf))


def set_range(range, values):
  logging.info(f'Setting Google Sheet range {range} to {values}')
  body = {
    'range': range,
    'majorDimension': 'ROWS',
    'values': [values]
  }
  _sheets_service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption='RAW', body=body).execute()


if __name__ == '__main__':
  print(get_ranges(['Settings!A2:A14']))
