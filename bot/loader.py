import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher



dotenv_path = os.path.join(os.path.dirname(__file__), 'utils', '.env')
load_dotenv(dotenv_path)

db_path = os.getenv('db_path')

storage = MemoryStorage()

bot = Bot(token = os.getenv('TOKEN'), parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
keywords_links = os.getenv("keywords_words")


