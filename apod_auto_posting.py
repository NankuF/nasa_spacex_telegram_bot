import argparse
import logging
import random
import sys
import textwrap as tw
import time
from typing import List

import environs
import telegram

from nasa_apod import fetch_nasa_apod_images

logging.basicConfig(format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s',
                    filename='errors.log', encoding='utf-8', level=logging.INFO)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apikey', type=str, required=True, help='ключ API')
    parser.add_argument('--token', type=str, required=True, help='токен телеграм-бота')
    parser.add_argument('--chat_id', type=str, required=True, help='@имя_телеграм_канала')
    parser.add_argument('--interval', type=int, default=4, required=True, help='интервал загрузки в часах')

    return parser


def create_message(images: List[dict], counter: int) -> str:
    image_data = {}
    if len(images[counter - 1].get('title', '')):
        image_data['title'] = images[counter - 1]['title']
    if 0 < len(images[counter - 1].get("explanation", '')) <= 1024:
        image_data['description'] = images[counter - 1]['explanation'].split('digg_url')[0].strip()
    if len(images[counter - 1].get('copyright', '')):
        image_data['copyright'] = images[counter - 1]['copyright']
    if len(images[counter - 1].get('date', '')):
        image_data['date'] = images[counter - 1]['date']

    message = ''
    for key, text in image_data.items():
        if key == 'title':
            message += f'<b>{text}</b>\n\n'
            continue
        if key == 'description':
            message += f'{text}\n\n'
            continue
        message += f'<b>{key}:</b> {text}\n'
    return tw.dedent(message)


def auto_posting(apikey: str, token: str, chat_id: str, interval: int):
    """
    Публикация фотографий APOD с определенным интервалом в часах.

    :param apikey: ключ API к сервису NASA.
    :param token: токен телеграм бота.
    :param chat_id: название чата для загрузки фото.
    :param interval: интервал между публикациями фото, в часах.
    """
    print('Start auto_posting')
    bot = telegram.Bot(token=token)

    images = []
    counter = 1
    hour = interval * 60 * 60
    while True:
        if not len(images) or counter > len(images):
            counter = 1
            images = fetch_nasa_apod_images(apikey=apikey)
            random.shuffle(images)

        message = create_message(images=images, counter=counter)
        try:
            bot.send_photo(chat_id=chat_id,
                           photo=images[counter - 1].get('hdurl', 'url'),
                           caption=message,
                           parse_mode=telegram.ParseMode.HTML)
        except telegram.error.BadRequest:
            counter += 1
            continue
        except telegram.error.RetryAfter as exc:
            time.sleep(exc.retry_after)
            continue
        time.sleep(hour)
        counter += 1


def main(chat_id: str, interval: int):
    env = environs.Env()
    env.read_env()
    apikey = env.str('NASA_API_KEY')
    token = env.str('TG_TOKEN')

    if len(sys.argv) == 1:
        auto_posting(apikey=apikey, token=token, chat_id=chat_id, interval=interval)
    else:
        parser = create_parser()
        namespace = parser.parse_args()
        auto_posting(apikey=namespace.apikey, token=namespace.token, chat_id=namespace.chat_id,
                     interval=namespace.interval)


if __name__ == '__main__':
    main(chat_id='@nasa_spacex_images_channel', interval=4)
