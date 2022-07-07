import argparse
import datetime
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


def fetch_nasa_epic_images(apikey: str, count: int, download: bool = False) -> [str]:
    """
    Получить изображения последних EPIC-фото NASA.
    EPIC - Earth Polychromatic Imaging Camera.
    :param apikey: ключ к сервисам NASA. (https://api.nasa.gov/)
    :param count: количество фотографий.
    :param download: скачать фотографии.
    """
    dirname = 'images/nasa_epic'
    os.makedirs(dirname, exist_ok=True)
    nasa_epic_path = Path(os.path.join(os.getcwd(), dirname))

    payload = {'api_key': apikey, }
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    resp = requests.get(url, params=payload)
    resp.raise_for_status()
    nasa_epic = resp.json()

    images_urls = []
    for image in nasa_epic[:count]:
        epic_datetime = datetime.datetime.strptime(image['identifier'][:8], '%Y%m%d')
        year, month, day = epic_datetime.year, epic_datetime.month, epic_datetime.day
        epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/png/{image["image"]}.png'
        if download:
            download_image(epic_url, nasa_epic_path, payload=payload)
        images_urls.append(epic_url)
    return images_urls


def main():
    env = environs.Env()
    env.read_env()

    parser = create_parser()
    namespace = parser.parse_args()
    nasa_api_key = namespace.apikey or env.str('NASA_API_KEY')
    count = namespace.count or env.int('EPIC_IMAGES_COUNT')

    fetch_nasa_epic_images(apikey=nasa_api_key, count=count, download=namespace.download)


if __name__ == '__main__':
    main()
