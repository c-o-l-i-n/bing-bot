import logging
import os
from operator import itemgetter
from retry import retry
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv()
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
NUM_RETRIES = 3
RETRY_DELAY = 2


_creds = GoogleCredentials.get_application_default().create_scoped(['https://www.googleapis.com/auth/spreadsheets'])
_sheets_service = build('sheets', 'v4', credentials=_creds)


@retry(tries=NUM_RETRIES, delay=RETRY_DELAY)
def get_range(range) -> list[str]:
  logging.info(f'Getting Google Sheet range {range}')
  result = _sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()['values']
  if len(result[0]) == 1:
    return list(map(lambda x : x[0], result))
  return result


@retry(tries=NUM_RETRIES, delay=RETRY_DELAY)
def get_ranges(ranges) -> list[list[list[str]]]:
  logging.info(f'Getting Google Sheet ranges {ranges}')
  asdf = _sheets_service.spreadsheets().values().batchGet(spreadsheetId=SPREADSHEET_ID, ranges=ranges).execute()['valueRanges']
  return list(map(itemgetter('values'), asdf))


@retry(tries=NUM_RETRIES, delay=RETRY_DELAY)
def set_range(range, values) -> None:
  logging.info(f'Setting Google Sheet range {range} to {values}')
  body = {
    'range': range,
    'majorDimension': 'ROWS',
    'values': [values]
  }
  _sheets_service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption='RAW', body=body).execute()


if __name__ == '__main__':
  print(get_ranges(['Settings!A2:A14']))
