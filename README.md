
# Telegram Bot

Bot itself — @ysda_kalugin_forecast_bot (currently disabled, due to explire of licence for YandexWeatherAPI)

For project implementation were used next API-s:

- [TelergamBotAPI](https://github.com/python-telegram-bot/python-telegram-bot)
- [YandexWeatherAPI](https://tech.yandex.ru/weather/)
- [BingSearchAPI](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/)

The bot can handle the following commands:
- /start — displays basic information about itself
- /help — displays detailed information about the itself, the possible forms of the request and supported commands
- /contains [city] — checks wether the bot can respond to requests about this city
- /feedback [message] — leave feedback to developers

The bot responds to the remaining commands that it cannot process them.

Normal messages are taken by the bot as requests regarding the weather. Processing of such requests takes place in several stages:
- parsing the incoming message, extracting the city and date from the message
- search of the forecast in the found city for the corresponding date
- search for a verse that matches the weather
- search for a picture that matches the found city and weather

Parsing of an incoming message is done using the [pymorphy2](https://pymorphy2.readthedocs.io/en/latest/) library in three steps:
- at first all words are transformed to the initial form
- among these words, it is searched for the first one, which is contained in cities for which you can make a request
- among these words, it is searched for the first word/phrase/combination of numbers corresponding to the date.

Implementation details:
- the bot responds to requests for weather only for the next 10 days (YandexWeatherAPI restriction)
- if the request contains words that can be regarded as a city, they will be regarded as a city, even if they originally carried a different meaning
