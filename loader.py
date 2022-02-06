from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
from database.db import Database


with open('config.json') as conf:
    config = json.load(conf)
    TOKEN = config['token']
    test_payload_token = config['test_payment_id']
    channel_id = config["channel_id"]
    price_for_newsletter = float(config["price_for_newsletter"])
    price_for_message = int(config["price_for_message"])
    # api_id = config['API_ID']
    # api_hash = config['API_HASH']


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
