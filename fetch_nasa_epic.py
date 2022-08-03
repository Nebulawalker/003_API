import os
import requests
import datetime
import random
import argparse

from dotenv import load_dotenv
from filesystem_helpers import download_images


NASA_EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural/images"


def fetch_nasa_epic(api_key: str, epic_api_url: str, image_count: int) -> None:
    payload = {"api_key": api_key}
    response = requests.get(epic_api_url, params=payload)
    response.raise_for_status()
    image_urls = []
    for photo_info in response.json():
        photo_date = photo_info["date"]
        date = datetime.datetime.fromisoformat(photo_date)
        formated_date = date.strftime("%Y/%m/%d")
        image_name = f"{photo_info['image']}.png"
        image_urls.append(
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{formated_date}/png/{image_name}"
        )

    random.shuffle(image_urls)
    download_images(image_urls[:image_count], "nasa_epic", payload)


def main():
    load_dotenv()
    nasa_api_key = os.getenv("NASA_API_KEY")

    parser = argparse.ArgumentParser(
        description="Скрипт скачивает фотографии NASA EPIC. \
        Без аргумента скачивает 4 фото \
        если указан аргумент, то скачивает указанное количество фото."
    )
    parser.add_argument(
        "-c", "--image_count",
        help="Количество фотографий",
        default=4,
        type=int
    )
    image_count = parser.parse_args().image_count

    fetch_nasa_epic(nasa_api_key, NASA_EPIC_API_URL, image_count)


if __name__ == "__main__":
    main()
