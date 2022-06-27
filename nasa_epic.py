import argparse
import datetime

from consts import NASA_API_KEY, HEADERS
from utils import download_image, fetch_json, create_dir


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', required=True, type=int)

    return parser


def fetch_nasa_epic_images(count: int):
    """
    Получить изображения последних EPIC-фото Nasa.
    EPIC - Earth Polychromatic Imaging Camera.
    :param count: количество фотографий.
    """
    nasa_epic_path = create_dir('images/nasa_epic')

    payload = {'api_key': NASA_API_KEY, }
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    nasa_epic_json = fetch_json(url, headers=HEADERS, payload=payload)

    for image in nasa_epic_json[:count]:
        epic_datetime = datetime.datetime.strptime(image['identifier'][:8], '%Y%m%d')
        year, month, day = epic_datetime.year, epic_datetime.month, epic_datetime.day
        epic_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/png/{image["image"]}.png'
        download_image(epic_url, nasa_epic_path, payload=payload, headers=HEADERS)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    fetch_nasa_epic_images(count=namespace.count)
