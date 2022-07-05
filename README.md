# Телеграм бот, публикующий фотографии космоса.

Порядок действий:

1. Скачайте проект:<br>

```commandline
git clone https://github.com/NankuF/nasa_spacex_telegram_bot.git
```

2. Создайте виртуальное окружение:<br>

```commandline
python -m venv venv
```

3. Перейдите в директорию:

```commandline
cd nasa_spacex_telegram_bot
```

4. Установите зависимости:<br>

```commandline
pip install -r requirements.txt
```

5. Создайте бота, канал и добавьте бота в канал с правами администратора.<br>
6. Создайте файл `.env` и укажите следующие переменные:<br>

```commandline
NASA_API_KEY='your_api_key'
TG_TOKEN='your_telegram_bot_token'
```

`NASA_API_KEY` - ключ для NASA создается здесь: https://api.nasa.gov/ <br>
`TG_TOKEN` - токен для телеграм-бота создается в телеграм-канале: https://t.me/botfather <br>

7. Используйте скрипт для автопостинга или ручного постинга фотографий в телеграм-канал.<br>

#### Автопостинг фотографий APOD в телеграм-канал.

`--apikey` - ключ к сервисам NASA.<br>
`--token` - токен телеграм-бота.<br>
`--chat_id` - имя вашего телеграм-канала, например ``@mychannel``.<br>
`--interval` - интервал между публикациями фотографий, в часах.<br>
Запуск (вариант 1):

```commandline
python apod_auto_posting.py --apikey "DEMO_KEY" --token "1234567800:FFHjtoY1pGrk9NGq19LBj1cbe08Hbui9WLx" --chat_id "@nasa_spacex_images_channel" --interval 1 
```
Запуск (вариант 2):
Измените скрипт, подставив свой канал и интервал в часах:<br>

```python
if __name__ == '__main__':
    main(chat_id='@nasa_spacex_images_channel', interval=4)
```
Запустите код:
```commandline
python apod_auto_posting.py
```

#### Ручной постинг фотографий APOD в телеграм-канал.

`--apikey` - ключ к сервисам NASA.<br>
`--token` - токен телеграм-бота.<br>
`--chat_id` - имя вашего телеграм-канала, например ``@mychannel``.<br>
Запуск (вариант 1):

```commandline
python apod_manual_posting.py --apikey "DEMO_KEY" --token "1234567800:FFHjtoY1pGrk9NGq19LBj1cbe08Hbui9WLx" --chat_id "@nasa_spacex_images_channel"
```

Запуск (вариант 2):
Измените скрипт, подставив свой канал:<br>
```python
if __name__ == '__main__':
    main(chat_id='@nasa_spacex_images_channel')
```
Запустите код:
```commandline
python apod_manual_posting.py
```
