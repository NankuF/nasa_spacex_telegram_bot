import argparse

from consts import HEADERS
from utils import download_image, fetch_json, create_dir


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', required=True, type=int)
    parser.add_argument('--id', type=str)

    return parser


def fetch_spacex_images(count: int, id: str = None):
    """
    Получить изображения с последних запусков Spacex.
    Если id запуска не указан, скачает фото с последнего запуска.
    :param count: количество фотографий.
    :param id: id запуска.
    """
    spacex_path = create_dir('images/spacex')

    url = 'https://api.spacexdata.com/v5/launches/'
    url = f'{url}{id}' if id else f'{url}latest'
    spacex_json = fetch_json(url, headers=HEADERS)

    for image_url in spacex_json['links']['flickr']['original'][:count]:
        download_image(image_url, spacex_path, headers=HEADERS)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    fetch_spacex_images(count=namespace.count, id=namespace.id)
