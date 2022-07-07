import argparse
import random
import time

import environs
import telegram

from utils import get_file_paths


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, required=True, help='путь до директории')
    parser.add_argument('--interval', type=int, required=True, help='интервал загрузки в часах')
    parser.add_argument('--token', type=str, help='токен телеграм-бота')
    parser.add_argument('--chat_id', type=str, help='@имя_телеграм_канала')

    return parser


def publish_auto(token: str, chat_id: str, dir_: str, interval: int):
    """
    Публикация фотографий из определенной директории с определенным интервалом в часах.
    :param token: токен телеграм бота.
    :param chat_id: название чата для загрузки фото.
    :param dir_: директория, откуда загружать фото. (пример: '/images/nasa_apod').
    :param interval: интервал между публикациями фото, в часах.
    """
    bot = telegram.Bot(token=token)

    image_paths = get_file_paths(path=dir_)
    random.shuffle(image_paths)
    counter = 1
    hours = interval * 60 * 60
    while True:
        if not len(image_paths):
            print('Нет фотографий.')
            break
        elif counter > len(image_paths):
            counter = 1
            random.shuffle(image_paths)
        with open(image_paths[counter - 1], 'rb') as image:
            bot.send_photo(chat_id=chat_id, photo=image)
        print('Фото опубликовано.')
        time.sleep(hours)
        counter += 1


def main():
    env = environs.Env()
    env.read_env()

    parser = create_parser()
    namespace = parser.parse_args()
    token = namespace.token or env.str('TG_TOKEN')
    chat_id = namespace.chat_id or env.str('CHAT_ID')

    publish_auto(token=token, chat_id=chat_id, dir_=namespace.dir, interval=namespace.interval)


if __name__ == '__main__':
    main()
