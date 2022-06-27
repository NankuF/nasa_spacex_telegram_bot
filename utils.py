import os
import urllib.parse
from pathlib import Path

import requests


def fetch_json(url: str, payload: dict = None, headers: dict = None) -> dict:
    """Получить json"""
    url = url
    resp = requests.get(url, headers=headers, params=payload)
    resp.raise_for_status()
    return resp.json()


def fetch_file_extension(url: str):
    """Получить расширение файла из url"""
    return os.path.splitext(url)[1]


def fetch_filename(url: str) -> str:
    """Получить имя файла из url, без расширения"""
    clear_path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    return os.path.splitext(clear_path)[0].split('/')[-1]


def create_dir(dirname: str) -> Path:
    """Создать директорию"""
    Path(os.path.join(os.sep, os.getcwd(), dirname)).mkdir(parents=True, exist_ok=True)
    return Path(os.path.join(os.sep, os.getcwd(), dirname))


def download_image(url: str, save_path: Path, payload=None, headers=None):
    """Скачать изображение"""
    url = url
    resp = requests.get(url, headers=headers, params=payload)
    filename = fetch_filename(url)

    with open(f'{os.path.join(os.sep, save_path, f"{filename}{fetch_file_extension(url)}")}', 'wb') as file:
        file.write(resp.content)
