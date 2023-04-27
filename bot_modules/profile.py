# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, access, groups
from template import simple_message

from aiogram import types
from aiogram.dispatcher import Dispatcher

# ---------------------------------------------------------
# БД
module_name = 'profile'

init_bd_cmds = ["""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    userName TEXT,
    userAccess TEXT,
    UNIQUE(user_id)
);""",
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_all}=+', '{user_access.user_access_group_all}=+');"
]

# ---------------------------------------------------------
# Сообщения

profile_message = '''
<b>📰 Профиль:</b> 

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

async def ProfileOpen(a_Message, state = None):
    user_info = GetUserInfo(a_Message.from_user.id)
    msg = profile_message
    if not user_info is None:
        msg = msg.replace('@user_id', str(user_info[0])).replace('@user_name', str(user_info[1]))
    return simple_message.WorkFuncResult(msg, item_access = user_info[2])

# ---------------------------------------------------------
# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_UserID, a_UserName):
    bot_bd.SQLRequestToBD("INSERT OR IGNORE INTO users (user_id, userName, userAccess) VALUES (?, ?, ?);", commit=True, param = (a_UserID, a_UserName, access.GetItemDefaultAccessForModule(module_name)))

def GetUserInfo(a_UserID):
    user_info = bot_bd.SQLRequestToBD('SELECT * FROM users WHERE user_id = ?', param = [a_UserID])
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
    dp.register_message_handler(simple_message.SimpleMessageTemplate(ProfileOpen, GetStartKeyboardButtons, GetAccess), text = user_profile_button_name)
