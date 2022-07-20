import requests
import argparse

from filesystem_helpers import download_images


SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/"
# 5eb87d47ffd86e000604b38a ID запуска с фотками


def fetch_spacex_launch(spacex_launch_url: str) -> None:
    response = requests.get(spacex_launch_url)
    response.raise_for_status()
    image_urls = response.json()["links"]["flickr"].get("original")

    if image_urls:
        download_images(image_urls, "spacex")
    else:
        print("Нет изображений в данном запуске")


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт скачивает фотографии SpaceX. Без аргумета \
        скачивает фото последнего запуска (если есть фото), \
        если указан аргумент, то скачивает фото указанного запуска"
    )
    parser.add_argument(
        "-id", "--flight_id",
        help="ID запуска"
    )
    launch_ID = parser.parse_args().flight_id

    try:
        if launch_ID:
            fetch_spacex_launch(f"{SPACEX_API_URL}{launch_ID}")
        else:
            fetch_spacex_launch(f"{SPACEX_API_URL}latest")
    except requests.exceptions.HTTPError as error:
        print(f"При выгрузке изображений возникла ошибка: {error}")


if __name__ == "__main__":
    main()
