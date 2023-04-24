# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, groups
from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
init_bd_cmds = ["""CREATE TABLE IF NOT EXISTS module_access(
    modName TEXT,
    modAccess TEXT,
    UNIQUE(modName)
);""",
"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('access', 'other=-');"
]

# ---------------------------------------------------------
# Сообщения

access_start_message = '''
<b> Права пользователей находятся в стадии разработки</b>

Пока можете воспользоваться хардкорным способом через запросы к БД
'''

request_start_message = '''
**Задайте запрос к БД**

Можете воспользоваться следующими шаблонами:
1. `SELECT * FROM users` - Все пользователи
'''

help_message = '''
Существует БД для работы с правами
`module_access (modName, modAccess)` - содержит права для модулей

modAccess - строка
''' + user_access.user_access_readme

access_button_name = "📰 Доступ пользователей"
sql_request_button_name = "📰 Запрос к БД для редактирования доступа"
help_button_name = "📰 Информация по редактированию доступа"

# ---------------------------------------------------------
# Работа с кнопками

def GetEditAccessKeyboardButtons(a_UserAccess):
    cur_buttons = [sql_request_button_name, help_button_name]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods, a_UserAccess) + cur_buttons)

# ---------------------------------------------------------
# Обработка сообщений

# Приветствие
async def AccessStart(a_Message):
    user_id = str(a_Message.from_user.id)
    user_access = GetUserAccess(a_Message.from_user.id)
    await bot.send_message(user_id, access_start_message, reply_markup = GetEditAccessKeyboardButtons(user_access))
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
    return [access_button_name]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(AccessStart, text = access_button_name)
    dp.register_message_handler(groups.RequestToBDTemplate(request_start_message), text = sql_request_button_name)
    dp.register_message_handler(groups.HelpTemplate(help_message, GetEditAccessKeyboardButtons), text = help_button_name)
