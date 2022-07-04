import argparse
import os
import sys
from pathlib import Path

import requests

from utils import download_image


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', required=True, type=int, help='количество фотографий для скачивания')
    parser.add_argument('--id', type=str, help='id запуска ракеты')
    parser.add_argument('--download', default=True, action=argparse.BooleanOptionalAction, help='cкачивать фото')

    return parser


def fetch_spacex_images(count: int, id: str = None, download: bool = True) -> [str]:
    """
    Получить изображения с последних запусков Spacex.
    Если id запуска ракеты не указан, скачает фото с последнего запуска.
    :param count: количество фотографий.
    :param id: id запуска.
    :param download: скачать фотографии.
    """
    dirname = 'images/spacex'
    os.makedirs(dirname, exist_ok=True)
    spacex_path = Path(os.path.join(os.getcwd(), dirname))

    url = 'https://api.spacexdata.com/v5/launches/'
    url = f'{url}{id}' if id else f'{url}latest'
    resp = requests.get(url)
    resp.raise_for_status()
    spacex = resp.json()

    images_urls = []
    for image_url in spacex['links']['flickr']['original'][:count]:
        if download:
            download_image(image_url, spacex_path)
        images_urls.append(image_url)
    return images_urls


def main(count: int, download: bool, id: str = None):
    if len(sys.argv) == 1:
        fetch_spacex_images(count=count, download=download, id=id)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        fetch_spacex_images(count=namespace.count, id=namespace.id, download=namespace.download)


if __name__ == '__main__':
    main(count=1, download=True, id='5eb87d42ffd86e000604b384')
