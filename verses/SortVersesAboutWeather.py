import config

import os
import glob
import shutil

def CreateDirectories():
    if not os.path.exists(config.VERSES_BY_WEATHER_FOLDER):
        os.makedirs(config.VERSES_BY_WEATHER_FOLDER)

    for condition in config.RUSSIAN_WEATHER_STATES:
        if not os.path.exists(config.VERSES_BY_WEATHER_FOLDER + '/' + condition):
            os.makedirs(config.VERSES_BY_WEATHER_FOLDER + '/' + condition)

def CutBigVerse(verse, condition, line):
    pass

def ParseVerses():
    verses_number = {condition : 0 for condition in config.RUSSIAN_WEATHER_STATES}
    for folder in os.listdir(config.VERSES_BY_AUTHORS_FOLDER):
        curr_folder = config.VERSES_BY_AUTHORS_FOLDER + '/' + folder
        for j, source in enumerate(os.listdir(curr_folder)):
            verse = curr_folder + '/' + source
            with open(verse, 'r') as file:
                text = file.readlines()
                text_as_line = ''.join(text)
                for condition in config.RUSSIAN_WEATHER_STATES:
                    if condition in text_as_line:
                        for i, line in enumerate(text):
                            if condition in line:
                                print(condition, source)
                                destination = os.path.join(config.VERSES_BY_WEATHER_FOLDER, condition,
                                                           str(verses_number[condition]) + '.txt')
                                start = max(0, i - 2)
                                end = min(len(text), start + 7)
                                part = text[start: end]
                                with open(destination, 'w') as lines:
                                    lines.writelines(part)
                                verses_number[condition] += 1
                                break


if __name__ == '__main__':
    CreateDirectories()
    ParseVerses()
