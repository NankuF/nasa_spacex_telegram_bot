from typing import List

import requests


def fetch_nasa_apod_images(apikey: str, count: int = 100) -> List[dict]:
    """
    Получить изображения APOD-фото NASA.
    APOD - Astronomy Picture of the Day.

    :param apikey: ключ к сервисам NASA. (https://api.nasa.gov/)
    :param count: количество фотографий в json, max 100.
    :return Список словарей с данными о фотографиях.
    """

    payload = {'api_key': apikey, 'count': count}
    url = f'https://api.nasa.gov/planetary/apod'
    resp = requests.get(url, params=payload)
    resp.raise_for_status()
    nasa_apod = resp.json()

    images = []
    for image in nasa_apod:
        images.append(image)
    return images
