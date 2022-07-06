import os
import urllib.parse
from pathlib import Path

import requests


def fetch_file_extension(url: str) -> str:
    """Получить расширение файла из url"""
    clear_path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    return os.path.splitext(clear_path)[1]


def fetch_filename(url: str) -> str:
    """Получить имя файла из url, без расширения"""
    clear_path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    return os.path.splitext(clear_path)[0].split('/')[-1]


def download_image(url: str, save_path: Path, payload=None):
    """Скачать изображение"""
    resp = requests.get(url, params=payload)
    filename = f'{fetch_filename(url)}{fetch_file_extension(url)}'
    path = os.path.join(os.sep, save_path, filename)

    with open(path, 'wb') as file:
        file.write(resp.content)


def get_file_paths(path: str) -> [str]:
    """Получает путь к файлам в директории и во вложенных директориях"""
    path = Path(os.path.join(os.sep, os.getcwd(), path))
    file_paths = []
    for top, dirs, files in os.walk(path):
        for file in files:
            file_paths.append(os.path.join(os.sep, top, file))
    return file_paths
