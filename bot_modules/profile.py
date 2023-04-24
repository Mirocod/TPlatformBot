# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, access, groups
from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
module_name = 'profile'

init_bd_cmds = ["""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    userName TEXT,
    UNIQUE(user_id)
);""",
f"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('{module_name}', 'other=+');"
]

# ---------------------------------------------------------
# Сообщения

profile_message = '''
<b>Профиль:</b>

<b>ID:</b> @user_id
<b>Имя:</b> @user_name
'''

user_profile_button_name = "📰 Профиль"

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons(a_UserGroups):
    mods = [start]
    return keyboard.MakeKeyboardForMods(mods, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# Отображение профиля пользователя
async def ProfileOpen(a_Message):
    user_id = str(a_Message.from_user.id)
    user_groups= groups.GetUserGroupData(user_id)
    if not user_access.CheckAccessString(GetAccess(), user_groups, user_access.AccessMode.VIEW):
        return await bot.send_message(user_id, access.access_denied_message, reply_markup = GetStartKeyboardButtons(user_groups))

    user_info = GetUserInfo(user_id)
    msg = profile_message
    if not user_info is None:
        msg = msg.replace('@user_id', str(user_info[0])).replace('@user_name', str(user_info[1]))
    await bot.send_message(user_id, msg, reply_markup = GetStartKeyboardButtons(user_groups))

# ---------------------------------------------------------
# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_UserID, a_UserName):
    bot_bd.SQLRequestToBD2Commit("INSERT OR IGNORE INTO users (user_id, userName) VALUES (?, ?);", a_UserID, a_UserName)

# Добавление пользователя, если он уже есть, то игнорируем
def GetUserInfo(a_UserID):
    user_info = bot_bd.SQLRequestToBD1('SELECT * FROM users WHERE user_id = ?', [a_UserID])
    print(user_info, str(user_info))
    if len(user_info) != 0:
        return user_info[0]
    return None

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(user_profile_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(ProfileOpen, text = user_profile_button_name)
