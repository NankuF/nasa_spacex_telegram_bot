import argparse
import datetime
import sys

from consts import NASA_API_KEY, HEADERS
from utils import download_image, fetch_json, create_dir


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', required=True, type=int)
    parser.add_argument('--download', required=False, default=True)

    return parser


def fetch_nasa_epic_images(count: int, download: bool = True) -> [str]:
    """
    Получить изображения последних EPIC-фото Nasa.
    EPIC - Earth Polychromatic Imaging Camera.
    :param count: количество фотографий.
    :param download: скачать фотографии.
    """
    nasa_epic_path = create_dir('images/nasa_epic')

    payload = {'api_key': NASA_API_KEY, }
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    nasa_epic_json = fetch_json(url, headers=HEADERS, payload=payload)

    images_urls = []
    for image in nasa_epic_json[:count]:
        epic_datetime = datetime.datetime.strptime(image['identifier'][:8], '%Y%m%d')
        year, month, day = epic_datetime.year, epic_datetime.month, epic_datetime.day
        epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/png/{image["image"]}.png'
        if download:
            download_image(epic_url, nasa_epic_path, payload=payload, headers=HEADERS)
        images_urls.append(epic_url)
    return images_urls


if __name__ == '__main__':
    if len(sys.argv) == 1:
        fetch_nasa_epic_images(2, download=True)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        fetch_nasa_epic_images(count=namespace.count)

