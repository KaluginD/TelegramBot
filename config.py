import pymorphy2 as pm

# telegram

YANDEX_WEATHER_TOKEN = 'HERE_IS_MY_YANDEX_WEATHER_TOKEN'
TELEGRAM_TOKEN = 'HERE_IS_MY_TELEGAM_TOKEN'
REGION_ID = 'https://api.weather.yandex.ru/v1/locations?lang='
GEOID_REQUEST = 'https://api.weather.yandex.ru/v1/locations/<geoid>/longterm'
FORECAST_REQUEST = 'https://api.weather.yandex.ru/v1/forecast'

START_MESSAGE = "Привет! Я бот, показывающий прогноз погоды. " \
                "Я могу показывать погоду на ближайшие 10 дней.\n" \
                "Я понимаю русский и английский, но отвечаю я пока только на русском. " \
                "Вы можете формулировать запросы в удобной для вас форме.\n" \
                "Я выдам вам прогноз, стишок про предстоящую погоду " \
                "и фото города, о котором вы спрашиваете(если смогу найти).\n" \
                "Для более подробной информации воспользуйтесь командой /help\n" \
                "Поговорите со мной!"

HELP_MESSAGE = "ForecastBot - это бот, который покаывает погоду на ближайшие 10 дней.\n" \
               "Вы можете выбрать город и дату, которые вас интересуют.\n" \
               "Вы можете формулировать запрос в любой удобной вам форме, " \
               "только пожалуйста, пишите название города без ошибок)\n" \
               "По умолчанию будет показан прогноз на завтра, но вы можете выбрать интересующий вас день недели, " \
               "или указать дату в формате ДД.ММ, или просто указать \"сегодня\", \"завтра\", " \
               "\"послезавтра\", \"через неделю\" или \"через X дней\".\n" \
               "Также я понимаю английский, со всеми аналогичными уточнениями даты, " \
               "правда, отвечаю я, пока что, только на русском.\n" \
               "Кроме этого, я постараюсь найти картинку, с выбраным вами городом и соответствующей погодой. " \
               "У меня это не всегда получается, подоборать наиболее релевантную картинку, но я честно стараюсь.\n" \
               "Поиск картинки может занять немного времени.\n" \
               "Еще я постараюсь подобрать стишок, соответствующий погоде. " \
               "Большую часть стихов я взял с сайта http://poemata.ru/poems/weather/\n" \
               "Определение соответствия стиха погоде делается автоматически, " \
               "поэтому иногда они получаются на совсем релевантными.\n" \
               "Вы можете узнать, есть ли интересующий вас город в моей базе с помощью команды /contains " \
               "(для корректной работы передайте этой команде только город)." \
               "Если вы хотите оставить отзыв или пожелание, используйте команду /feedback\n" \
               "Приятного пользования!"

CANNOT_FIND_CITY_MESSAGE = 'Извините, я не нашел город, о котором вы говорите :('
CANNOT_FIND_VERSE_MESSAGE = 'К сожалению, у меня нет стиха про такую погоду.'
UNKNOWN_COMMAND = 'Извините, я не поддерживаю такую команду.'
FEEDBACK_MESSAGE = 'Спасибо за ваш отзыв!'
FOUND_CITY_MESSAGE = 'Я могу показывать прогноз в этом городе.'
NOT_FOUND_CITY_MESSAGE = 'Я не могу показывать прогноз в этом городе.'

WEATHER_STATES = {
    "clear": "ясно",
    "mostly-clear": "малооблачно",
    "partly-cloudy": "малооблачно",
    "overcast": "пасмурно",
    "partly-cloudy-and-light-rain": "небольшой дождь",
    "partly-cloudy-and-rain": "дождь",
    "overcast-and-rain": "сильный дождь",
    "overcast-thunderstorms-with-rain": "гроза",
    "cloudy": "облачно с прояснениями",
    "cloudy-and-light-rain": "небольшой дождь",
    "overcast-and-light-rain": "небольшой дождь",
    "cloudy-and-rain": "дождь",
    "overcast-and-wet-snow": "дождь со снегом",
    "partly-cloudy-and-light-snow": "небольшой снег",
    "partly-cloudy-and-snow": "снег",
    "overcast-and-snow": "снегопад",
    "cloudy-and-light-snow": "небольшой снег",
    "overcast-and-light-snow": "небольшой снег",
    "cloudy-and-snow": "снег"
}

RUSSIAN_WEATHER_STATES = list(set(WEATHER_STATES.values()))


def format_weather(city, date, weather):
    if not weather:
        return "Извините, я могу показывать погоду только на 10 дней вперед :("

    morph = pm.MorphAnalyzer()
    try:
        parse_city = morph.parse(city)[0]
        city = parse_city.inflect({'loct'})[0].title()
    except Exception:
        city = city.title()
    day_weather = weather['parts']['day']
    night_weather = weather['parts']['night']
    condition = WEATHER_STATES[day_weather['condition']]
    condition = condition[0].capitalize() + condition[1:]
    return "Вот погода в {} на {}.{}:\n" \
           "Макс. температура днем: {}°\n" \
           "Мин. температура ночью: {}°\n" \
           "Вероятность осадков: {}%\n" \
           "{}".format(city, date.day, date.month,
                       day_weather['temp_max'],
                       night_weather['temp_min'],
                       day_weather['prec_prob'],
                       condition)


# verses download

VERSES_BY_AUTHORS_FOLDER = 'verses_by_authors'

# verses parsing


VERSES_BY_WEATHER_FOLDER = 'verses_by_weather'

NEAREST_WEATHER_STATES_FOR_PICTURES = {
    "clear": "clear",
    "mostly-clear": "clear",
    "partly-cloudy": "cloudy",
    "overcast": "cloudy",
    "partly-cloudy-and-light-rain": "rain",
    "partly-cloudy-and-rain": "rain",
    "overcast-and-rain": "rain",
    "overcast-thunderstorms-with-rain": "rain",
    "cloudy": "cloudy",
    "cloudy-and-light-rain": "rain",
    "overcast-and-light-rain": "rain",
    "cloudy-and-rain": "rain",
    "overcast-and-wet-snow": "rain",
    "partly-cloudy-and-light-snow": "snow",
    "partly-cloudy-and-snow": "snow",
    "overcast-and-snow": "snow",
    "cloudy-and-light-snow": "snow",
    "overcast-and-light-snow": "snow",
    "cloudy-and-snow": "snow"
}

NEAREST_WEATHER_STATES_FOR_VERSES = {
    'малооблачно': 'пасмурно',
    'небольшой дождь': 'дождь',
    'сильный дождь': 'дождь',
    'облачно с прояснениями': 'пасмурно',
    'дождь со снегом': 'дождь',
    'небольшой снег': 'снег',
}

WEEK_DAYS_RU = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресение'
]

WEEK_DAYS_EN = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]

SIMPLE_DAY = [
    'сегодня',
    'сейчас',
    'today',
    'now',
    'завтра',
    'послезавтра',
    'tomorrow'
]

DAY = [
    'day',
    'days',
    'день',
    'дни'
]
