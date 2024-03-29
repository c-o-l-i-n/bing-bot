# NO LONGER USED

import requests
import pdf2image
from datetime import datetime
from io import BytesIO
import groupme_image_service
from send_message import send_message


def send_daily_schedule() -> None:
  season_start_date = (8, 22)
  season_end_date = (12, 5)
  todays_date = (datetime.today().month, datetime.today().day)

  # if we are not in marching band season, stop the program
  if not (season_start_date <= todays_date <= season_end_date):
    return

  # get previous daily schedule url
  try:
    with open('previous_daily_schedule_url.txt') as f:
      previous_daily_schedule_url = f.read()
  except:
    previous_daily_schedule_url = ''

  # get today's daily schedule
  daily_schedule_request = requests.get('https://go.osu.edu/dailyschedule')
  current_daily_schedule_url = daily_schedule_request.history[-1].url

  # if daily schedule url hasn't changed, send disappointing message
  if current_daily_schedule_url == previous_daily_schedule_url:
    send_message("the daily schedule hasn't been updated since last time :(")
    return

  # convert daily schedule PDF to list of images (1 image per page)
  pdf_page_images = pdf2image.convert_from_bytes(daily_schedule_request.content)

  # convert 1st page image to byte array
  image_byte_array = BytesIO()
  pdf_page_images[0].save(image_byte_array, format='png')
  image_byte_array = image_byte_array.getvalue()

  # upload image to GroupMe image service
  groupme_image_url = groupme_image_service.get_groupme_image_url_from_bytes(image_byte_array)

  # send daily schedule
  send_message("here is today's rehearsal schedule!", groupme_image_url)

  # update previous daily schedule url
  with open('previous_daily_schedule_url.txt', 'w') as f:
    f.write(current_daily_schedule_url)
  

if __name__ == '__main__':
  send_daily_schedule()
