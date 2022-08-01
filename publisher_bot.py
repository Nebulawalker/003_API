import telegram
from telegram import InputMediaPhoto
import os
import random
import time
import argparse

from dotenv import load_dotenv

TELEGRAM_IMAGES_IN_ALBUM_LIMIT = 10


def get_record_for_album(
    path: str,
    file_name: str,
    caption: str = None
) -> InputMediaPhoto:

    with open(os.path.join(path, file_name), "rb") as media:
        return InputMediaPhoto(media=media, caption=caption)


def publish_post(
    bot: telegram.Bot,
    chat_id: str,
    image_count: int,
    periodicity_in_hours: float,
    image_path: str,
    caption: str
) -> None:

    periodicity_in_seconds = periodicity_in_hours * 3600
    connection_attempts = 1

    file_names = os.listdir(image_path)

    image_count = min(
        len(file_names),
        image_count,
        TELEGRAM_IMAGES_IN_ALBUM_LIMIT
    )

    print(
        f"Запущена автоматическая публикация постов в Telegram:\n"
        f"Периодичность (часы): {periodicity_in_hours}\n"
        f"Количество изображений в посте: {image_count}\n"
        f"Каталог с фото: {image_path}\n"
        f"Подпись: '{caption}'\n\n"
    )

    while True:
        file_names = os.listdir(image_path)
        random.shuffle(file_names)
        file_names[:image_count]
        album_for_publication = []

        for index, file in enumerate(file_names, 1):
            caption_ = caption if index == 1 else None
            album_for_publication.append(
                get_record_for_album(image_path, file, caption_)
            )

        try:
            bot.send_media_group(
                chat_id=chat_id,
                media=album_for_publication)
            print("Опубликован пост...")
        except telegram.error.NetworkError as e:
            if connection_attempts == 1:
                print(
                    f"Нет соединения с сервером:\n{e}\n\n"
                    f"Попытка подключения № {connection_attempts}...\n\n"
                )
                time.sleep(1)
                connection_attempts += 1
            else:
                print(
                    f"Нет соединения с сервером:\n{e}\n\n"
                    f"Попытка подключения № {connection_attempts}...\n\n"
                )
                time.sleep(30)
                connection_attempts += 1
            continue

        time.sleep(periodicity_in_seconds)
        connection_attempts = 1


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = telegram.Bot(token=telegram_token)

    parser = argparse.ArgumentParser(
        description="Скрипт запускает автоматическую публикацию постов в Telegram.\
            При запуске без параметров использует значения по умолчанию."
    )

    parser.add_argument(
        "-i", "--image_count",
        help="Количество изображений в посте (по умолчанию 6)",
        default=6, type=int
    )
    parser.add_argument(
        "-p", "--periodicity_in_hours",
        help="Периодичность (часы) (по умолчанию 4)",
        default=4, type=float
    )
    parser.add_argument(
        "-isp", "--image_source_path",
        help="Каталог с фото (по умолчанию 'image')",
        default="image"
    )
    parser.add_argument(
        "-c", "--caption",
        help="Подпись (по умолчанию 'Подборка фотографий про космос!!!')",
        default="Очередная подборка фотографий про космос!!!")

    image_count = parser.parse_args().image_count
    periodicity_in_hours = parser.parse_args().periodicity_in_hours
    image_source_path = parser.parse_args().image_source_path
    caption = parser.parse_args().caption

    try:
        publish_post(
            bot,
            chat_id,
            image_count,
            periodicity_in_hours,
            image_source_path,
            caption
        )
    except KeyboardInterrupt:
        print("\nПубликация постов остановлена.")
        exit()


if __name__ == "__main__":
    main()
