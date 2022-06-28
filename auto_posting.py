import argparse
import random
import sys
import time
from datetime import datetime

import environs
import telegram

from utils import read_dirs

env = environs.Env()
env.read_env()
token = env.str('TG_TOKEN')
chat_id = env.str('TG_CHAT_ID')


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', required=True, type=str)
    parser.add_argument('--hour', required=True, type=int, default=4)
    parser.add_argument('--chat_id', required=False, type=str, default=chat_id)

    return parser


def auto_posting(dir_: str, interval: int, chat_id=chat_id):
    """
    Публикация фотографий из определенной директории с определенным интервалом в часах.
    :param dir_: директория, откуда загружать фото. (пример: '/images/nasa_apod').
    :param interval: интервал между публикациями фото, в часах.
    :param chat_id: id чата для загрузки фото.
    """
    bot = telegram.Bot(token=token)

    images = read_dirs(path=dir_)
    random.shuffle(images)
    now, update = datetime.now(), datetime.now()
    n = 0
    while True:
        time.sleep(60)
        now = datetime.now()
        if now.hour - update.hour >= interval:
            if len(images):
                bot.send_photo(chat_id=chat_id, photo=open(images[n], 'rb'))
                print('Фото опубликовано')
                update = datetime.now()
                if n >= len(images):
                    n = 0
                    random.shuffle(images)
                else:
                    n += 1
            else:
                print('Нет фотографий.')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        auto_posting('images/nasa_apod', interval=1)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        auto_posting(dir_=namespace.dir, interval=namespace.hour)
