import config

import requests
from bs4 import BeautifulSoup as bs
import os

def LoadPoemata():
    POETRY = 'http://poemata.ru'
    WEATHER = '/poems/weather/'
    PAGE_2 = '?page=2'

    verses_pages = []
    for page in [POETRY + WEATHER, POETRY + WEATHER + PAGE_2]:
        req = requests.get(page)
        soup = bs(req.text, 'lxml')
        ol = soup.find_all('ol')[1]

        for line in ol.find_all('a', href=True):
            verses_pages.append(POETRY + line['href'])

    verses = []
    for page in verses_pages:
        req = requests.get(page)
        verse_soup = bs(req.text, 'lxml')
        verse = verse_soup.find('div', "preline").get_text()
        verses.append(verse)

    if not os.path.exists(config.VERSES_BY_AUTHORS_FOLDER):
        os.makedirs(config.VERSES_BY_AUTHORS_FOLDER)
    folder = config.VERSES_BY_AUTHORS_FOLDER + '/' + 'poemata'
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, verse in enumerate(verses):
        with open(folder + '/' + str(i) + '.txt', 'w') as f:
            f.writelines(verse)

if __name__ == '__main__':
    LoadPoemata()