from telebot import TeleBot

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

import json
import urllib.request

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Origin': 'https://yandex.ru',
    'Referer': 'https://yandex.ru/',
}

API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'

def main_job():
    Log.info("Starting main job")
    
    phrase, phrase_type = PhrasesClass(SheetPhrases, 'phrases').get_random_phrase_and_type()
    response = ''
    already_sent = AlreadySentClass(SheetPivot, 'alreadysent')
    while response == '' or already_sent.check_if_already_sent(response):
        payload = {"query": phrase, "intro": phrase_type, "filter": 1}
        params = json.dumps(payload).encode('utf8')
        req = urllib.request.Request(API_URL, data=params, headers=headers)
        response_json = urllib.request.urlopen(req).read().decode('utf8')
        response_dict = json.loads(response_json)
        response = response_dict["query"] + response_dict["text"]
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