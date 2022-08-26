import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from settings import UnsolicitedMessageSetting, get_settings
from custom_message_senders.send_air_piss import send_air_piss
from custom_message_senders.send_alex import send_alex
from custom_message_senders.send_bezos import send_bezos
from custom_message_senders.send_call_wawa import send_call_wawa
from custom_message_senders.send_drink_water import send_drink_water
from custom_message_senders.send_elon import send_elon
from custom_message_senders.send_h import send_h
from custom_message_senders.send_katie_paid import send_katie_paid
from custom_message_senders.send_meme import send_meme
from custom_message_senders.send_now_you_see_me import send_now_you_see_me
from custom_message_senders.send_sky_piss import send_sky_piss
from custom_message_senders.send_the_car_quote import send_the_car_quote


timezone = 'America/New_York'
logging.info(f'Creating scheduler with timezone "{timezone}"')
scheduler = BlockingScheduler(timezone=timezone)

logging.info(f'Defining scheduled jobs')


# get whether setting is turned on
def settings(setting: UnsolicitedMessageSetting):
    SETTING = get_settings()
    is_turned_on = SETTING[setting]
    if not is_turned_on:
        logging.info('Setting is turned off')
    return is_turned_on


# send "H" at a random time between 9am and 10pm
@scheduler.scheduled_job(name='send_h', trigger='cron', hour=9, jitter=46800)
def send_h_job():
    if settings(UnsolicitedMessageSetting.H):
        send_h()


# send a meme at a random time between 9am and 10pm
# OFF
@scheduler.scheduled_job(name='send_meme', trigger='cron', hour=9, jitter=46800)
def send_meme_job():
    if settings(UnsolicitedMessageSetting.MEME):
        send_meme(message_text='meme of the day')


# send a "Now You See Me" message at a random time between 9am and 10pm
@scheduler.scheduled_job(name='send_now_you_see_me', trigger='cron', hour=9, jitter=46800)
def send_now_you_see_me_job():
    if settings(UnsolicitedMessageSetting.NOW_YOU_SEE_ME):
        send_now_you_see_me()


# reminds Hanna to drink water at a random time between 9am and 10pm
@scheduler.scheduled_job(name='send_drink_water', trigger='cron', hour=9, jitter=46800)
def send_drink_water_job():
    if settings(UnsolicitedMessageSetting.HANNA_DRINK_WATER):
        send_drink_water()


# send Jeff Bezos message at a random time between 5pm and 8pm
# OFF
@scheduler.scheduled_job(name='send_bezos', trigger='cron', day_of_week='mon-fri', hour=17, jitter=10800)
def send_bezos_job():
    if settings(UnsolicitedMessageSetting.JEFF_BEZOS):
        send_bezos()


# send Elon message at a random time between 5pm and 8pm
@scheduler.scheduled_job(name='send_elon', trigger='cron', day_of_week='mon-fri', hour=17, jitter=10800)
def send_elon_job():
    if settings(UnsolicitedMessageSetting.ELON_MUSK):
        send_elon()


# check for rain every 30 minutes between 9am and 10pm
@scheduler.scheduled_job(name='send_sky_piss', trigger='cron', hour='9-21', minute='15,45')
def send_sky_piss_job():
    if settings(UnsolicitedMessageSetting.RAIN):
        send_sky_piss()


# check for high humidity every 30 minutes between 9am and 10pm
@scheduler.scheduled_job(name='send_air_piss', trigger='cron', hour='9-21', minute='0,30')
def send_air_piss_job():
    if settings(UnsolicitedMessageSetting.HUMIDITY):
        send_air_piss()


# send "guys, has anyone called wawa??" at a random time between 3am and 6am every Saturday
@scheduler.scheduled_job(name='send_call_wawa', trigger='cron', day_of_week='sat', hour=3, jitter=10800)
def send_call_wawa_job():
    if settings(UnsolicitedMessageSetting.WAWA):
        send_call_wawa()


# send a rotated image of Alex Gonzalez at a random time between 9am and 10pm
# OFF
@scheduler.scheduled_job(name='send_alex', trigger='cron', hour=9, jitter=46800)
def send_alex_job():
    if settings(UnsolicitedMessageSetting.ROTATE_ALEX):
        send_alex()


# send a quote from "The Car" at a random time between 9am and 10pm
@scheduler.scheduled_job(name='send_the_car_quote', trigger='cron', hour=9, jitter=46800)
def send_the_car_quote_job():
    if settings(UnsolicitedMessageSetting.THE_CAR_QUOTE):
        send_the_car_quote(is_quote_of_the_day=True)


logging.info(f'Starting scheduler')
scheduler.start()
