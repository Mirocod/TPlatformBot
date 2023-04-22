# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

log_start_message = 'Бот успешно запущен!'

import os
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from bot_sys import config, log, bot_bd
from bot_modules import profile, start

storage = MemoryStorage()
bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage = storage)

mods = [profile, start]

init_bd_cmd = []
for m in mods:
    m.RegisterHandlers(dp)
    c = m.GetInitBDCommands()
    if not c is None:
        init_bd_cmd += c

# Первичаня инициализация базы данных
bot_bd.BDExecute(init_bd_cmd)

if __name__ == '__main__':
    os.system('clear')
    os.system('cls')
    log.Success(log_start_message)

executor.start_polling(dp)
