import datetime
import string

import config
import logging
import pymorphy2 as pm

logging.getLogger("pymorphy2").setLevel(logging.WARNING)

def ParseCity(args, russian_cities, english_cities):
    geoid = None
    options = [' '.join(args[i: i + 2]) for i in range(len(args) - 1)] + args
    for word in options:
        if len(word) < 3:
            continue
        if word in russian_cities:
            geoid = russian_cities[word]
        if word in english_cities:
            geoid = english_cities[word]
        if geoid:
            return geoid
    return geoid

def ParseDate(args):
    basic_date = date = datetime.datetime.now()
    for i, j in zip(args[:-1], args[1:]):
        try:
            day = int(i)
            if day < 10 and j in config.DAY:
                date = datetime.datetime(date.year, date.month, date.day + day)
        except Exception:
            pass
        if date != basic_date:
            break
    for i in args:
        try:
            day, month = int(i[:2]), int(i[2:])
            if month > 12:
                day, month = month, day
            date = datetime.datetime(date.year, month, day)
        except Exception:
            pass
        if date != basic_date:
            break
    for word in args:
        if word in config.WEEK_DAYS_RU:
            move = (config.WEEK_DAYS_RU.index(word) - date.weekday()) % 7
            date += datetime.timedelta(days=move)
        if word in config.WEEK_DAYS_EN:
            move = (config.WEEK_DAYS_EN.index(word) - date.weekday()) % 7
            date += datetime.timedelta(days=move)
        if word in config.SIMPLE_DAY:
            if word in config.SIMPLE_DAY[:4]:
                continue
            move = 1
            i = args.index(word)
            if word == 'послезавтра' or (i > 0 and args[i - 1] == 'after'):
                move += 1
            date += datetime.timedelta(days=move)
        if word in ['неделя', 'week']:
            date += datetime.timedelta(days=7)
        if date != basic_date:
            break
    return date


def ParseMessage(message, russian_cities, english_cities, logger, chat_id):
    punctuation = dict.fromkeys(string.punctuation)
    punctuation.pop('-', None)
    table = str.maketrans(punctuation)
    message = message.translate(table)
    morph = pm.MorphAnalyzer()
    args = [morph.parse(word.lower())[0].normal_form for word in message.split()]
    logger.info("Requset from {}: Message normalized form: {}".format(chat_id, ' '.join(args)))
    geoid = ParseCity(args, russian_cities, english_cities)
    date = ParseDate(args)
    logger.info("Requset from {}: geoid: {}, date: {}".format(chat_id, geoid, date))

    return geoid, date
