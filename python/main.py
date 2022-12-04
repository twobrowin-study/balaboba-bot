from telebot import TeleBot
from balaboba import Balaboba

import sys

import schedule
import time

from log import Log

from settings import BotToken, TimingUpdateTime

from settings import SheetGroups, SheetPhrases
from settings import SheetMainText, SheetPictures
from settings import SheetPivot

from timing import Timing
from groups import GroupsClass
from phrases import PhrasesClass
from pictures import PicturesClass
from maintext import MainTextClass
from alreadysent import AlreadySentClass

from datetime import datetime

Bot = TeleBot(BotToken, parse_mode='Markdown')

def main_job():
    Log.info("Starting main job")
    
    phrase, phrase_type = PhrasesClass(SheetPhrases, 'phrases').get_random_phrase_and_type()
    response = ''
    already_sent = AlreadySentClass(SheetPivot, 'alreadysent')
    while response == '' or already_sent.check_if_already_sent(response):
        response = Balaboba().balaboba(phrase, text_type=phrase_type)
    already_sent.write_text(response)

    date_until = datetime.strptime(Timing.get_until_date(), "%Y-%m-%d %H:%M").date()
    today_date = datetime.today().date()
    days_left = (date_until - today_date).days

    message = MainTextClass(SheetMainText, 'maintext').get_main_text().format(
        balaboba_responce = response,
        days_left = days_left
    )

    pic = PicturesClass(SheetPictures, 'pictures').get_today_image()

    for id in GroupsClass(SheetGroups, 'groups').get_id_list():
        Bot.send_photo(id, photo=pic, caption=message)

    Log.info("Main job done")

class JobClass():
    def __init__(self) -> None:
        self.__create_job()
    
    def __create_job(self) -> None:
        at = Timing.get_at_everyday_time()
        until = Timing.get_until_date()
        self.job = schedule.every(1).day.at(at).until(until).do(main_job)
        Log.info(f"Created job to run at {at} until {until}")
    
    def update_job(self) -> None:
        schedule.cancel_job(self.job)
        Log.info(f"Canceled job")
        self.__create_job()
Job = JobClass()

def timing_update_job():
    Timing.update()

    if Timing.check_if_should_change():
        Timing.write_changed()
        Job.update_job()

schedule.every(TimingUpdateTime).seconds.do(timing_update_job)

if __name__ == '__main__':
    Log.info("Starting...")

    if len(sys.argv) >= 2 and sys.argv[1] in ['debug', '--debug', '-D']:
        Log.info(Bot.get_me())
        main_job()
    else:
        while 1:
            schedule.run_pending()
            time.sleep(1)

    Log.info("Done. Goodby!")