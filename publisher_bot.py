import telegram
from telegram import InputMediaPhoto
import os
import random
import time
import argparse


from dotenv import load_dotenv


def publish_post(
    bot: telegram.Bot,
    image_count: int,
    periodicity_in_hours: float,
    image_path: str,
    caption: str
) -> None:

    periodicity_in_seconds = periodicity_in_hours * 3600
    connection_attempts = 1

    file_names = os.listdir(image_path)
    if len(file_names) < image_count:
        image_count = len(file_names)
    elif image_count > 10:
        image_count = 10

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
        with open(f"{image_path}{file_names[0]}", "rb") as media:
            album_for_publication = [
                InputMediaPhoto(media=media, caption=caption)]

        for index in range(1, image_count):
            with open(f"{image_path}{file_names[index]}", "rb") as media:
                album_for_publication.append(
                    InputMediaPhoto(
                        media=media
                    )
                )

        try:
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
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
    bot = telegram.Bot(token=telegram_token)

    parser = argparse.ArgumentParser(
        description="Скрипт запускает автоматическую публикацию постов в Telegram.\
            При запуске без параметров использует значения по умолчанию."
    )

    parser.add_argument(
        "-i", "--image_count",
        help="Количество изображений в посте (по умолчанию 4)",
        default=4, type=int
    )
    parser.add_argument(
        "-p", "--periodicity_in_hours",
        help="Периодичность (часы) (по умолчанию 4)",
        default=4, type=float
    )
    parser.add_argument(
        "-ip", "--image_path",
        help="Каталог с фото (по умолчанию 'image/')",
        default="image/"
    )
    parser.add_argument(
        "-c", "--caption",
        help="Подпись (по умолчанию 'Подборка фотографий про космос!!!')",
        default="Очередная подборка фотографий про космос!!!")

    image_count = parser.parse_args().image_count
    periodicity_in_hours = parser.parse_args().periodicity_in_hours
    image_path = parser.parse_args().image_path
    caption = parser.parse_args().caption

    try:
        publish_post(
            bot,
            image_count,
            periodicity_in_hours,
            image_path,
            caption
        )
    except KeyboardInterrupt:
        print("\nПубликация постов остановлена.")
        exit()


if __name__ == "__main__":
    main()
