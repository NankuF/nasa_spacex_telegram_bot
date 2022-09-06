import argparse
import logging
import random
import textwrap as tw
import time
from typing import List

import environs
import telegram

from nasa_apod import fetch_nasa_apod_images

logging.basicConfig(format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s',
                    filename='errors.log', level=logging.INFO)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apikey', type=str, help='ключ API')
    parser.add_argument('--token', type=str, help='токен телеграм-бота')
    parser.add_argument('--chat_id', type=str, help='@имя_телеграм_канала')
    parser.add_argument('--interval', type=int, help='интервал загрузки в часах')

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


def publish_auto(apikey: str, token: str, chat_id: str, interval: int):
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
    hours = interval * 60 * 60
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
        time.sleep(hours)
        counter += 1


def main():
    env = environs.Env()
    env.read_env()

    parser = create_parser()
    namespace = parser.parse_args()
    apikey = namespace.apikey or env.str('NASA_API_KEY')
    token = namespace.token or env.str('TG_TOKEN')
    chat_id = namespace.chat_id or env.str('CHAT_ID')
    interval = namespace.interval or env.int('INTERVAL')

    publish_auto(apikey=apikey, token=token, chat_id=chat_id, interval=interval)


if __name__ == '__main__':
    main()
