
# Telegram Bot

Сам бот — @ysda_kalugin_forecast_bot 

Для выполнения задания были искользованы следующие API:

- [TelergamBotAPI](https://github.com/python-telegram-bot/python-telegram-bot)
- [YandexWeatherAPI](https://tech.yandex.ru/weather/)
- [BingSearchAPI](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/)

Бот умеет обрабатывать следующие команды:
- /start — выводит основную информацию оо боте
- /help — выводит подробную информацию о боте, о возможных формах запроса и поддерживаемых командах
- /contains [city] — позволяет проверить, может ли бот отвечать на запросы об этом городе
- /feedback [message] — позволяет оставить обратную связь разработчикам

На остальные команды бот отвечает, что не может их обработать.

Обычные сообщения бот воспринимает как запросы касательно погоды. Обработка таких запросов проходит в несколько этапов:
- парсинг входящего сообщения, извлечение из сообдщения города и даты
- поиск прогноза в найденом городе на соответствующую дату
- поиск стиха, соответсвующего полученой погоде
- поиск картинки, соответствующей найденым городу и погоде

Парсинг входящего сообщения делается с помощью библиотеки [pymorphy2](https://pymorphy2.readthedocs.io/en/latest/) в три этапа:
- сперва все слова приводятся в начальную форму
- среди этих слов ищется первое, которое содержится в городах, по которым можно делать запрос
- вреди этих слов ищется первое слово/словосочетание/комбинация чисел, соответствующее дате

Тонкости:
- бот отвечает на запросы о погоде только на ближайшие 10 дней(ограничение YandexWeatherAPI)
- если в запросе есть слова, которые могут быть расценены как город, они будут расценены как город, даже если изначально несли другой смысл
