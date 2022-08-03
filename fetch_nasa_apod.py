import requests
import os
import argparse

from dotenv import load_dotenv
from filesystem_helpers import download_images, get_extension

NASA_APOD_API_URL = "https://api.nasa.gov/planetary/apod"
SUPPORTED_IMAGES = (".jpg", ".png", ".gif")


def fetch_nasa_apod(api_key: str, apod_api_url: str, image_count: int) -> None:
    payload = {
        "api_key": api_key,
        "count": image_count
        }
    response = requests.get(apod_api_url, params=payload)
    response.raise_for_status()
    records = response.json()

    image_urls = []
    for record in records:
        url = record.get("url")
        if url and get_extension(url) in SUPPORTED_IMAGES:
            image_urls.append(url)

    download_images(image_urls, "nasa_apod")


def main():
    load_dotenv()
    nasa_api_key = os.getenv("NASA_API_KEY")

    parser = argparse.ArgumentParser(
        description="Скрипт скачивает фотографии NASA Astronomy Picture of the Day (APOD). \
        Без аргумента скачивает 1 фото, \
        если указан аргумент, то скачивает указанное количество фото. \
        Поддерживает скачивание только следующих форматов : gif, jpg, png."
    )
    parser.add_argument(
        "-c", "--image_count",
        help="Количество фотографий",
        default=1,
        type=int
    )
    image_count = parser.parse_args().image_count

    try:
        fetch_nasa_apod(nasa_api_key, NASA_APOD_API_URL, image_count)
    except requests.exceptions.HTTPError as error:
        print(f"При выгрузке изображений возникла ошибка: {error}")


if __name__ == "__main__":
    main()
