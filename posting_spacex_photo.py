import argparse
import random
import sys

import environs
import telegram

from spacex import fetch_spacex_images
from utils import read_dirs

env = environs.Env()
env.read_env()
token = env.str('TG_TOKEN')
chat_id = env.str('TG_CHAT_ID')


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', type=str)
    parser.add_argument('--chat_id', required=False, type=str, default=chat_id)

    return parser


def posting_spacex_photo(id: str = None, chat_id=chat_id):
    """
    Публикует одну фотографию по id запуска ракеты , либо из директории.
    :param id: id запуска ракеты
    :param chat_id: id чата для загрузки фото.
    """
    bot = telegram.Bot(token=token)

    images = read_dirs('images/spacex')
    random.shuffle(images)
    images_urls = fetch_spacex_images(count=5, id=id, download=False)
    if id:
        bot.send_photo(chat_id=chat_id, photo=random.choice(images_urls))
    else:
        bot.send_photo(chat_id=chat_id, photo=random.choice(images))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        posting_spacex_photo(id='5eb87cf2ffd86e000604b344')
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        posting_spacex_photo(id=namespace.id)
