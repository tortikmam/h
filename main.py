import sys
import argparse
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
parser = argparse.ArgumentParser()
parser.add_argument("toponym_to_find", nargs='+')
args = parser.parse_args()

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": ' '.join(args.toponym_to_find),
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('error')
    sys.exit(1)
# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
x, y = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
x1, y1 = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": f'{abs(x - x1) * 0.5},{abs(y - y1) * 0.5}',
    'pt': f'{toponym_longitude},{toponym_lattitude},flag',
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()