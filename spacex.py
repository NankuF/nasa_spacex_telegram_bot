import argparse
import os
from pathlib import Path

import environs
import requests

from utils import download_image


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, help='количество фотографий для скачивания')
    parser.add_argument('--id', type=str,
                        help='если указан, скачает фото по id запуска ракеты, иначе скачает фото с последнего запуска')
    parser.add_argument('--download', action='store_true', help='скачать фотографии')

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
    spacex_launch = resp.json()

    images_urls = []
    for image_url in spacex_launch['links']['flickr']['original'][:count]:
        if download:
            download_image(image_url, spacex_path)
        images_urls.append(image_url)
    return images_urls


def main():
    env = environs.Env()
    env.read_env()

    parser = create_parser()
    namespace = parser.parse_args()
    count = namespace.count or env.int('SPACEX_IMAGES_COUNT')

    fetch_spacex_images(count=count, id=namespace.id, download=namespace.download)


if __name__ == '__main__':
    main()
