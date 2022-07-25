import requests
import os
from urllib.parse import urlparse
from typing import Iterable
from image_compressor import compress_image


TELEGRAM_IMAGE_SIZE_LIMIT = 20971520


def download_images(
    urls: Iterable,
    service: str,
    payload: dict = {"": ""}
) -> None:
    os.chdir(os.path.dirname(__file__))
    os.makedirs("image", exist_ok=True)
    for index, url in enumerate(urls):
        response = requests.get(url, params=payload)
        response.raise_for_status()
        file_extention = get_extension(url)
        path = os.path.join(
            "image",
            f"{service}_{index}{file_extention}"
        )
        with open(path, "wb") as file:
            file.write(response.content)

        if os.path.getsize(path) > TELEGRAM_IMAGE_SIZE_LIMIT:
            compress_image(path)


def get_extension(url):
    parsed_url = urlparse(url)
    file_path = os.path.splitext(parsed_url.path)
    file_extension = file_path[1]
    return file_extension
