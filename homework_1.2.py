# Зарегистрироваться на https://openweathermap.org/api и написать функцию,
# которая получает погоду в данный момент для города, название которого получается через input.
# https://openweathermap.org/current
import requests
import os
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()


def get_weather(city, appid):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&lang=ru&units=metric'
    return requests.get(url)


key = os.getenv('openweather')
city = 'Samara'
# city = 'Samara'
r = get_weather(city, key)
pprint(dict(r.json()))
key = os.getenv('openweather')
city = input('Please insert City: ')
# city = 'Samara'
r = get_weather(city, key)
pprint(dict(r.json()))


