import json
import logging

import requests

import GetForecast
import GetPicture
import GetVerse
import ParseMessage
import config
import string
import pymorphy2 as pm
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

GEOID_REQUEST = config.GEOID_REQUEST
YANDEX_WEATHER_TOKEN = config.YANDEX_WEATHER_TOKEN
REGION_ID = config.REGION_ID
TELEGRAM_TOKEN = config.TELEGRAM_TOKEN

logging.getLogger("pymorphy2").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.updater").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.dispatcher").setLevel(logging.WARNING)

class WeatherBot(object):
    def __init__(self):
        self.russian_cities = self.get_cities('ru_RU')
        self.english_cities = self.get_cities('en_US')
        self.geoid_dict = {geoid: {'ru': city} for city, geoid in self.russian_cities.items()}
        for city, geoid in self.english_cities.items():
            if geoid in self.geoid_dict:
                self.geoid_dict[geoid]['en'] = city
            else:
                self.geoid_dict[geoid] = {'en': city}
        self.feedback = []

        self.updater = Updater(token=TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        start_handler = CommandHandler('start', self.start)
        help_handler = CommandHandler('help', self.help)
        forecast_handler = MessageHandler(Filters.text, self.forecast_request)
        contains_handler = CommandHandler('contains', self.contains, pass_args=True)
        feedback_handler = CommandHandler('feedback', self.answer, pass_args=True)
        unknown_handler = MessageHandler(Filters.command, self.unknown)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(forecast_handler)
        self.dispatcher.add_handler(feedback_handler)
        self.dispatcher.add_handler(contains_handler)
        self.dispatcher.add_handler(unknown_handler)

    def run(self):
        self.updater.start_polling()

    @staticmethod
    def get_cities(language):
        req = requests.get(REGION_ID + language, headers={'X-Yandex-API-Key': YANDEX_WEATHER_TOKEN})
        results = json.loads(req.text)
        cities = {line['name'].lower(): line['geoid'] for line in reversed(results)}
        return cities

    @staticmethod
    def start(bot, update):
        message = config.START_MESSAGE
        bot.send_message(chat_id=update.message.chat_id,
                         text=message)

    @staticmethod
    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=config.HELP_MESSAGE)

    def forecast_request(self, bot, update):
        chat_id = update.message.chat_id
        self.logger.info("Requset from {}: {}".format(chat_id,
                                                      update.message.text))
        try:
            geoid, date = ParseMessage.ParseMessage(
                update.message.text, self.russian_cities, self.english_cities, self.logger, chat_id)
            city_ru, city_en = self.geoid_dict[geoid]['ru'].title(), self.geoid_dict[geoid]['en'].title()
            if not city_ru:
                city_ru = city_en
            if not city_en:
                city_en = city_ru
            weather = GetForecast.GetForecast(geoid, self.logger, chat_id, date)
            condition = weather['parts']['day']['condition']
            verse = GetVerse.GetVerse(condition, self.logger, chat_id)
        except Exception:
            bot.send_message(chat_id=update.message.chat_id,
                             text=config.CANNOT_FIND_CITY_MESSAGE)
            return
        picture = None
        try:
            picture = GetPicture.GetPicture(city_en, condition, self.logger, chat_id)
        except Exception:
            pass
        forecast = config.format_weather(city_ru, date, weather)
        result = forecast + '\n\n' + verse
        bot.send_message(chat_id=update.message.chat_id,
                         text=result)
        if picture:
            bot.send_photo(chat_id=update.message.chat_id,
                           photo=picture)

    def contains(self, bot, update, args):
        punctuation = dict.fromkeys(string.punctuation)
        punctuation.pop('-', None)
        table = str.maketrans(punctuation)
        args = str(args)
        args = args.translate(table)
        morph = pm.MorphAnalyzer()
        city = morph.parse(args)[0][0]
        if city in self.english_cities.keys() or city in self.russian_cities.keys():
            bot.send_message(chat_id=update.message.chat_id,
                             text=config.FOUND_CITY_MESSAGE)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=config.NOT_FOUND_CITY_MESSAGE)

    @staticmethod
    def answer(bot, update, args):
        feedback = ' '.join(args)
        print(feedback)
        bot.send_message(chat_id=update.message.chat_id,
                         text=config.FEEDBACK_MESSAGE)

    @staticmethod
    def unknown(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=config.UNKNOWN_COMMAND)


def main():
    bot = WeatherBot()
    bot.run()


if __name__ == '__main__':
    main()
