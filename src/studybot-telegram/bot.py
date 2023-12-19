import logging
import grequests

from dotenv import load_dotenv
load_dotenv()

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.misc.throttling import ThrottlingMiddleware
from aiogram import Dispatcher, Bot
from aiogram.utils import executor

from os import getenv, system
from modules.handlers import *


system('cls')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=getenv('BOT_TOKEN'), parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=register_all_handlers(dp))
