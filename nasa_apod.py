import argparse

from consts import NASA_API_KEY, HEADERS
from utils import download_image, fetch_json, create_dir


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', required=True, type=int)

    return parser


def fetch_nasa_apod_images(count: int):
    """
    Получить изображения последних APOD-фото Nasa.
    APOD - Astronomy Picture of the Day.
    :param count: количество фотографий.
    """
    nasa_apod_path = create_dir('images/nasa_apod')

    payload = {'api_key': NASA_API_KEY, 'count': count, }
    url = f'https://api.nasa.gov/planetary/apod'
    nasa_apod_json = fetch_json(url, headers=HEADERS, payload=payload)

    for image in nasa_apod_json:
        download_image(image['hdurl'], nasa_apod_path, payload=payload, headers=HEADERS)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    fetch_nasa_apod_images(count=namespace.count)
