import argparse
import sys

from consts import HEADERS
from utils import download_image, fetch_json, create_dir


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', required=True, type=int)
    parser.add_argument('--id', type=str)
    parser.add_argument('--download', required=False, default=True)

    return parser


def fetch_spacex_images(count: int, id: str = None, download: bool = True) -> [str]:
    """
    Получить изображения с последних запусков Spacex.
    Если id запуска ракеты не указан, скачает фото с последнего запуска.
    :param count: количество фотографий.
    :param id: id запуска.
    :param download: скачать фотографии.
    """
    spacex_path = create_dir('images/spacex')

    url = 'https://api.spacexdata.com/v5/launches/'
    url = f'{url}{id}' if id else f'{url}latest'
    spacex_json = fetch_json(url, headers=HEADERS)

    images_urls = []
    for image_url in spacex_json['links']['flickr']['original'][:count]:
        if download:
            download_image(image_url, spacex_path, headers=HEADERS)
        images_urls.append(image_url)
    return images_urls


if __name__ == '__main__':
    if len(sys.argv) == 1:
        fetch_spacex_images(count=5, download=True)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        fetch_spacex_images(count=namespace.count, id=namespace.id)

