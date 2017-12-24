import config

import requests
import json
import datetime

def GetForecast(geoid, logger, chat_id, date=datetime.datetime.now()):
    logger.info("Requset from {}: Searching for weather at {} for {}".format(chat_id, geoid, date))
    geoid = str(geoid)
    limit = max((date - datetime.datetime.now()).days, 2)
    if limit > 10:
        return None
    params = {'geoid': geoid, 'lang': 'ru_RU', 'limit': limit}
    req = requests.get(config.FORECAST_REQUEST, params=params,
                       headers={'X-Yandex-API-Key': config.YANDEX_WEATHER_TOKEN})
    result = json.loads(req.text)
    forecast = result['forecasts'][limit - 1]
    return forecast

if __name__ == '__main__':
    GetForecast()
