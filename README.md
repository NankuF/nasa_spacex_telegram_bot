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
`NASA_API_KEY` - ключ для Nasa создается здесь: https://api.nasa.gov/ <br>
`TG_TOKEN` - токен для телеграм-бота создается в телеграм-канале: https://t.me/botfather <br>
7. Запустите один из скриптов для скачивания фотографий.(см. ниже)<br>
#### Скрипты для скачивания фотографий (Windows)

Результат: скачает указанное количество фотографий.<br>

<b>Spacex:</b><br>
`--сount` - количество фотографий.<br>
`--id` - id запуска ракеты. Если id не указать, скачает фото с последнего запуска (если есть).<br>
`--download` - скачать фото (по умолчанию).<br>
`--no-download` - не скачивать фото.<br>
```commandline
python spacex.py --count 1 --id 5eb87cf2ffd86e000604b344
```

<b>NASA_APOD:</b><br>
`--apikey` - ключ к сервисам NASA.<br>
`--сount` - количество фотографий.<br>
`--download` - скачать фото (по умолчанию).<br>
`--no-download` - не скачивать фото.<br>
```commandline
python nasa_apod.py --apikey "DEMO_KEY" --count 1 
```

<b>NASA_EPIC:</b><br>
`--apikey` - ключ к сервисам NASA.<br>
`--сount` - количество фотографий.<br>
`--download` - скачать фото (по умолчанию).<br>
`--no-download` - не скачивать фото.<br>
```commandline
python nasa_epic.py --apikey "DEMO_KEY" --count 1 --no-download
```
6. Используйте скрипт для автопостинга в телеграм, либо используйте скрипт для ручного
   постинга фотографий Spacex.(см. ниже)<br>
#### Автопостинг фотографий в телеграм-канал.
`--apikey` - ключ к сервисам NASA.<br>
`--token` - токен телеграм-бота.<br>
`--chat_id` - имя вашего телеграм-канала, например ``@mychannel``.<br>
`--interval` - интервал между публикациями фотографий, в часах.<br>

```commandline
python auto_posting.py --apikey "DEMO_KEY" --token "1234567800:FFHjtoY1pGrk9NGq19LBj1cbe08Hbui9WLx" --chat_id "@nasa_spacex_images_channel" --interval 1 
```

#### Ручной постинг фотографий Spacex в телеграм-канал.

`--token` - токен телеграм-бота.<br>
`--id` - id запуска ракеты.<br>
`--chat_id` - имя вашего телеграм-канала, например ``@mychannel``.<br>

```commandline
python posting_spacex_photo.py --token "1234567800:FFHjtoY1pGrk9NGq19LBj1cbe08Hbui9WLx" --id 5eb87d42ffd86e000604b384 --chat_id "@nasa_spacex_images_channel"
```

Примечание: id запуска ракеты можно получить из json, перейдя по ссылке:<br>
https://api.spacexdata.com/v5/launches/past