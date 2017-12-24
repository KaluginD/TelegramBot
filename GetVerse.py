import config

import os
import glob
import random

def GetVerse(condition, logger, chat_id):
    logger.info("Requset from {}: Searching for verse for condition: {}".format(chat_id, condition))
    if condition in config.WEATHER_STATES.keys():
        condition = config.WEATHER_STATES[condition]
    if condition in config.NEAREST_WEATHER_STATES_FOR_VERSES.keys():
        condition = config.NEAREST_WEATHER_STATES_FOR_VERSES[condition]
    if condition not in config.RUSSIAN_WEATHER_STATES:
        return config.CANNOT_FIND_VERSE_MESSAGE
    condition_folder = os.path.join('verses', config.VERSES_BY_WEATHER_FOLDER, condition)
    verses = len(os.listdir(condition_folder))
    if verses == 0:
        return config.CANNOT_FIND_VERSE_MESSAGE
    verse_number = random.randint(0, verses - 1)
    verse_name = os.path.join(condition_folder, str(verse_number) + '.txt')
    with open(verse_name, 'r') as file:
        verse = file.readlines()
    return ''.join(verse)

