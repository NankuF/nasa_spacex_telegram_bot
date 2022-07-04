import argparse
import random
import sys

import environs
import telegram

from spacex import fetch_spacex_images
from utils import get_file_paths


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True, help='токен телеграм-бота')
    parser.add_argument('--chat_id', type=str, required=True, help='@имя_телеграм_канала')
    parser.add_argument('--id', type=str, required=True, help='id запуска ракеты')

    return parser


def posting_spacex_photo(token: str, chat_id: str, id: str = None):
    """
    Публикует одну фотографию по id запуска ракеты , либо из директории.
    :param token: токен телеграм бота.
    :param chat_id: название чата для загрузки фото.
    :param id: id запуска ракеты.
    """
    bot = telegram.Bot(token=token)

    image_paths = get_file_paths('images/spacex')
    random.shuffle(image_paths)
    images_urls = fetch_spacex_images(count=1, id=id, download=True)
    if id:
        bot.send_photo(chat_id=chat_id, photo=random.choice(images_urls))
    else:
        if len(image_paths):
            with open(random.choice(image_paths), 'rb') as image:
                bot.send_photo(chat_id=chat_id, photo=image)
        else:
            print('Нет фотографий.')


def main(chat_id: str, id: str = None):
    env = environs.Env()
    env.read_env()
    token = env.str('TG_TOKEN')

    if len(sys.argv) == 1:
        posting_spacex_photo(token=token, chat_id=chat_id, id=id)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        posting_spacex_photo(token=namespace.token, chat_id=namespace.chat_id, id=namespace.id)


if __name__ == '__main__':
    main(chat_id='@nasa_spacex_images_channel', id='5eb87cf2ffd86e000604b344')
