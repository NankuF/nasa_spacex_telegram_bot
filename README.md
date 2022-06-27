# Телеграм бот, публикующий фотографии космоса.

## Запуск скриптов (Windows)

Результат: скачает указанное количество фотографий.<br>

<b>Spacex:</b><br>
-с - количество фотографий.<br>
--id - id запуска. Если id не указать, скачает фото с последнего запуска (если есть).<br>

```commandline
 python .\spacex.py -c 1 --id 
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