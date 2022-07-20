import requests
import os
from urllib.parse import urlparse
from typing import Iterable


def download_images(urls: Iterable, service: str) -> None:
    os.makedirs("image", exist_ok=True)
    for index, url in enumerate(urls):
        response = requests.get(url)
        response.raise_for_status()
        file_extention = get_extension(url)
        with open(f"image/{service}_{index}{file_extention}", "wb") as file:
            file.write(response.content)


def get_extension(url):
    parsed_url = urlparse(url)
    file_path = os.path.splitext(parsed_url.path)
    file_extension = file_path[1]
    return file_extension
