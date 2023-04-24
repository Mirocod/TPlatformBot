# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import bot_bd, log, config, keyboard
from bot_modules import start
from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
init_bd_cmds = []

# ---------------------------------------------------------
# Сообщения

# ---------------------------------------------------------
# Работа с кнопками

# ---------------------------------------------------------
# Обработка сообщений

# ---------------------------------------------------------
# Работа с базой данных 


# ---------------------------------------------------------
# API

def GetUserAccess(a_UserID):
    return None

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

# Доступные кнопки
def GetButtonNames(a_UserAccess):
    return []

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    return
