import config

import json
import random
import http.client, urllib.parse

BING_KEY = '02053fab192a404e82363a70bacbfc7b'

def GetPicture(city, condition, logger, chat_id):
    host = "api.cognitive.microsoft.com"
    path = "/bing/v7.0/images/search/"

    condition = config.NEAREST_WEATHER_STATES_FOR_PICTURES[condition]
    # condition = ' '.join(condition.split('-'))
    term = '{} weather in {}'.format(condition, city)

    def BingWebSearch(search):
        "Performs a Bing Web search and returns the results."

        headers = {'Ocp-Apim-Subscription-Key': BING_KEY}
        conn = http.client.HTTPSConnection(host)
        query = urllib.parse.quote(search)
        conn.request("GET", path + "?q=" + query, headers=headers)
        response = conn.getresponse()
        headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
        return headers, response.read().decode("utf8")

    if len(BING_KEY) == 32:

        logger.info('Requset from {}: Searching for picture: {}'.format(chat_id, term))

        headers, result = BingWebSearch(term)
        result = json.loads(result)
        try:
            img_url = result['value'][random.randrange(5)]['contentUrl']
            return img_url
        except Exception:
            print('no picture for {}'.format(term))

    else:

        print("Invalid Bing Search API subscription key!")
        print("Please paste yours into the source code.")
    return None


if __name__ == '__main__':
    GetPicture('London', 'overcast and snow')