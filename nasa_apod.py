import argparse
import os
from pathlib import Path

import environs
import requests

from utils import download_image


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apikey', type=str, help='ключ к сервисам NASA')
    parser.add_argument('--count', type=int, help='количество фотографий для скачивания')
    parser.add_argument('--download', action='store_true', help='скачать фотографии')

    return parser


def fetch_nasa_apod_images(apikey: str, count: int, download: bool = False) -> [str]:
    """
    Получить изображения последних APOD-фото NASA.
    APOD - Astronomy Picture of the Day.
    :param apikey: ключ к сервисам NASA. (https://api.nasa.gov/)
    :param count: количество фотографий.
    :param download: скачать фотографии.
    """
    dirname = 'images/nasa_apod'
    os.makedirs(dirname, exist_ok=True)
    nasa_apod_path = Path(os.path.join(os.getcwd(), dirname))

    payload = {'api_key': apikey, 'count': count, }
    url = f'https://api.nasa.gov/planetary/apod'
    resp = requests.get(url, params=payload)
    resp.raise_for_status()
    nasa_apod = resp.json()

    images_urls = []
    for image in nasa_apod:
        if download:
            download_image(image['hdurl'], nasa_apod_path, payload=payload)
        images_urls.append(image['hdurl'])
    return images_urls


def main():
    env = environs.Env()
    env.read_env()

    parser = create_parser()
    namespace = parser.parse_args()
    nasa_api_key = namespace.apikey or env.str('NASA_API_KEY')
    count = namespace.count or env.int('APOD_IMAGES_COUNT')

    fetch_nasa_apod_images(apikey=nasa_api_key, count=count, download=namespace.download)


if __name__ == '__main__':
    main()
