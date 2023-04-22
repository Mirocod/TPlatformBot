# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

log_start_message = 'Бот успешно запущен!'

import os
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from bot_sys import config, log
from bot_modules import user

storage = MemoryStorage()
bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

user.RegisterHandlers(dp)

if __name__ == '__main__':
    os.system('clear')
    os.system('cls')
    log.Success(log_start_message)

executor.start_polling(dp)
