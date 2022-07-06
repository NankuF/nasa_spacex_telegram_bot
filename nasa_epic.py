import argparse
import datetime
import os
import sys
from pathlib import Path

import environs
import requests

from utils import download_image


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apikey', required=True, type=str, help='ключ к сервисам NASA')
    parser.add_argument('--count', required=True, type=int, help='количество фотографий для скачивания')
    parser.add_argument('--download', default=True, action=argparse.BooleanOptionalAction, help='cкачивать фото')

    return parser


def fetch_nasa_epic_images(apikey: str, count: int, download: bool = True) -> [str]:
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


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    nasa_api_key = env.str('NASA_API_KEY')

    if len(sys.argv) == 1:
        fetch_nasa_epic_images(nasa_api_key, count=1, download=True)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        fetch_nasa_epic_images(apikey=namespace.apikey, count=namespace.count, download=namespace.download)
