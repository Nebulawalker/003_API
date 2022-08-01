# Размещение фотографий космоса в Telegram
Набор скриптов предназначенных для скачивания фотографий с 3-х сервисов:
SpaceX, Nasa APOD, NASA EPIC. Размещение фотографий в Telegram.

## Как установить
Для написания скрипта использовался __Python 3.10.0__
Инструмент для управления зависимостями __Poetry__

1. Склонировать репозиторий.
2. Создать виртуальное окружение.
3. Установить зависимости:
```
poetry install
```
4. Переименовать файл .env_example в .env

```bash
mv .env_example .env
```

5. Отредактировать файл .env, 
Пример .env:
```
NASA_API_KEY=1234567890abcdefghijklmnopqrstuvwxyz1234
TELEGRAM_TOKEN=958423683:AAEAtJ5Lde5YYfkjergber
TELEGRAM_CHAT_ID=@your_chat_id
```
*Как получить TELEGRAM_TOKEN: https://way23.ru/регистрация-бота-в-telegram.html

*Где получить NASA_API_KEY: https://api.nasa.gov/

*TELEGRAM_CHAT_ID можно посмотреть в описании канала

6. Активировать виртуальное окружение:

```bash
poetry shell
```

## Запуск
__1. Для скачивания фотографий:__

__1.1 Сервис SpaceX (fetch_spacex_launch.py)__

Скрипт скачивает фотографии SpaceX. Без аргумета скачивает фото последнего запуска (если есть), если указан ID, то скачивает фото указанного запуска.
```bash
usage: fetch_spacex_launch.py [-h] [-id FLIGHT_ID]
options:
-h, --help            show this help message and exit
-id FLIGHT_ID, --flight_id FLIGHT_ID
                        ID запуска
```
__Пример (в этом запуске точно есть фотографии):__

```bash
python fetch_spacex_launch.py -id 5eb87d47ffd86e000604b38a
```

    
__1.2 Сервис NASA Astronomy Picture of the Day (APOD) (fetch_nasa_apod.py)__

Скрипт скачивает фотографии NASA Astronomy Picture of the Day (APOD).
Без аргумета скачивает 1 фото, если указан аргумент, то скачивает указанное количество фото.
Поддерживает скачивание только следующих форматов : gif, jpg, png.

```bash
usage: fetch_nasa_apod.py [-h] [-c IMAGE_COUNT]

options:
-h, --help            show this help message and exit
-c IMAGE_COUNT, --image_count IMAGE_COUNT
                        Количество фотографий
```
__Пример:__
```bash
python fetch_nasa_apod.py -c 30
```

Скачает 30 случайных фотографий.
    
__1.3 Сервис NASA EPIC (fetch_nasa_epic.py)__

```bash
usage: fetch_nasa_epic.py [-h] [-c IMAGE_COUNT]

Скрипт скачивает фотографии NASA EPIC. Без аргумета скачивает 4 фото,
если указан аргумент, то скачивает указанное количество фото.

options:
  -h, --help            show this help message and exit
  -c IMAGE_COUNT, --image_count IMAGE_COUNT
                        Количество фотографий
```

```bash
python fetch_nasa_epic.py -c 5
```
Скачает 5 фото.

__2. Для публикации постов с фотографиями (publisher_bot)__

Скрипт запускает автоматическую публикацию постов в Telegram.
Если запустить без параметров, то будут использованы параметры по умолчанию.
```bash
usage: publisher_bot.py [-h] [-i IMAGE_COUNT]
                        [-p PERIODICITY_IN_HOURS]
                        [-ip IMAGE_PATH]
                        [-c CAPTION]
options:
  -h, --help            show this help message and exit
  -i IMAGE_COUNT, --image_count IMAGE_COUNT
                        Количество изображений в посте (по умолчанию 4)
  -p PERIODICITY_IN_HOURS, --periodicity_in_hours PERIODICITY_IN_HOURS
                        Периодичность (часы) (по умолчанию 4)
  -ip IMAGE_PATH, --image_path IMAGE_PATH
                        Каталог с фото (по умолчанию 'image/')
  -c CAPTION, --caption CAPTION
                        Подпись (по умолчанию 'Подборка фотографий про космос!!!')
```
__Пример:__

```bash
python publisher_bot.py -i 5 -p 2 -c Тест
```

Запустит публикацию каждые 2 часа, с альбомом из 5 фотографий, и подписью 'Тест'

В случае отсутствия(разрыва) соединения с сервером скрипт попытается отправить пост снова. В первой попытке сразу же, последующие попытки будут происходить каждые 30 секунд.

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
