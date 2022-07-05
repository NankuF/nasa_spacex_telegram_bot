import argparse
import sys
import time

import environs
import telegram

from apod_auto_posting import create_message
from nasa_apod import fetch_nasa_apod_images


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apikey', type=str, required=True, help='ключ API')
    parser.add_argument('--token', type=str, required=True, help='токен телеграм-бота')
    parser.add_argument('--chat_id', type=str, required=True, help='@имя_телеграм_канала')

    return parser


def posting_apod_photo(apikey: str, token: str, chat_id: str):
    """
    Публикует одну фотографию в телеграм-канал.

    :param apikey: ключ API к сервису NASA.
    :param token: токен телеграм бота.
    :param chat_id: название чата для загрузки фото.
    """
    bot = telegram.Bot(token=token)

    counter = 1
    images = fetch_nasa_apod_images(apikey=apikey, count=1)
    message = create_message(images=images, counter=counter)
    run_loop = True
    while run_loop:
        try:
            bot.send_photo(chat_id=chat_id,
                           photo=images[counter - 1].get('hdurl', 'url'),
                           caption=message,
                           parse_mode=telegram.ParseMode.HTML)
            run_loop = False
        except telegram.error.BadRequest:
            images = fetch_nasa_apod_images(apikey=apikey, count=1)
            message = create_message(images=images, counter=counter)
            continue
        except telegram.error.RetryAfter as exc:
            time.sleep(exc.retry_after)
            continue


def main(chat_id: str):
    env = environs.Env()
    env.read_env()
    apikey = env.str('NASA_API_KEY')
    token = env.str('TG_TOKEN')

    if len(sys.argv) == 1:
        posting_apod_photo(apikey=apikey, token=token, chat_id=chat_id)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        posting_apod_photo(apikey=namespace.apikey, token=namespace.token, chat_id=namespace.chat_id)


if __name__ == '__main__':
    main(chat_id='@nasa_spacex_images_channel')
