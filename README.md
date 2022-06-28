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
3. Установите зависимости:<br> 
```commandline
pip install -r requirements.txt
```
3. Создайте бота, канал и добавьте бота в канал администратором.<br>
4. Создайте файл `.env` и укажите следующие переменные:<br>
```commandline
NASA_API_KEY='your_api_key'
TG_TOKEN='your_telegram_bot_token'
TG_CHAT_ID='@your_chat_or_channel'
```
   Ключ для Nasa создается здесь: ``https://api.nasa.gov/`` <br>
   Токен для телеграм-бота создается в телеграме, в канале ``@BotFather``<br>
   Chat_id - ссылка на телеграм-канал, например ``@mychannel``<br>
5. Запустите один из скриптов для скачивания фотографий.(см. ниже)<br>
#### Скрипты для скачивания фотографий (Windows)

Результат: скачает указанное количество фотографий.<br>

<b>Spacex:</b><br>
-с - количество фотографий.<br>
--id - id запуска ракеты. Если id не указать, скачает фото с последнего запуска (если есть).<br>

```commandline
 python .\spacex.py -c 1 --id 5eb87cf2ffd86e000604b344
```

<b>NASA_APOD:</b><br>
-с - количество фотографий.<br>

```commandline
 python .\nasa_apod.py -c 1 
```

<b>NASA_EPIC:</b><br>
-с - количество фотографий.<br>

```commandline
 python .\nasa_epic.py -c 1 
```
6. Используйте скрипт для автопостинга в телеграм, указав нужную директорию, либо используйте скрипт для ручного
   постинга фотографий Spacex.(см. ниже)<br>
#### Автопостинг фотографий в телеграм-канал.

-h - интервал между публикациями фотографий, в часах.<br>
-d - директория с которой загружаются фотографии.<br>

```commandline
python .\auto_posting.py -h 4 -d /images/nasa_apod 
```

#### Ручной постинг фотографий Spacex в телеграм-канал.

-id - id запуска ракеты.<br>

```commandline
python .\posting_spacex_photo.py -id 5eb87d42ffd86e000604b384 
```

Примечание: id запуска ракеты можно получить из json, обратившись по ссылке
`https://api.spacexdata.com/v5/launches/past`