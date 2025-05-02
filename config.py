from dotenv import load_dotenv
from os import getenv
from aiogram import Bot

load_dotenv()

DB_URL = getenv('DB_URL')  # Ввести сюда свою ссылку на БД
bot = Bot(getenv('BOT'))  # Ввести сюда свой api-ключ от бота
admin = int(getenv('ADMIN'))  # Ввести telegram-id(именно id, не username) админа