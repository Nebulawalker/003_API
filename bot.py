import telegram
import os

from dotenv import load_dotenv


load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=telegram_token)

bot.send_message(chat_id="@cosmos_photos", text="Это все, что я пока могу....:(")

photo = open("./image/nasa_apod_0.jpg", "rb")

bot.send_photo(chat_id="@cosmos_photos", photo=photo)