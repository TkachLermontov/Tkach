import argparse
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
parser = argparse.ArgumentParser()
parser.add_argument('--size', nargs=2, type=float)
parser.add_argument('adress', nargs='+')
args = parser.parse_args()
size_list = [str(i) for i in args.size]
toponym_to_find = " ".join(args.adress)


def function(top_find, spn_list=None):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": top_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass
    # Преобразуем ответ в json-объект
    if spn_list is None:
        spn_list = [0.005, 0.005]
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(spn_list),
        "pt": ",".join([toponym_longitude, toponym_lattitude]) + "," + "pm2rdl",
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    return response


resp = function(toponym_to_find, size_list)
Image.open(BytesIO(resp.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
