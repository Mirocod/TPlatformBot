# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, groups
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

class FSMRequestToBD(StatesGroup):
    sqlRequest = State()

# ---------------------------------------------------------
# БД
table_name = 'module_access'
module_name = 'access'

init_bd_cmds = [f"""CREATE TABLE IF NOT EXISTS {table_name}(
    modName TEXT,
    modAccess TEXT,
    UNIQUE(modName)
);""",
f"INSERT OR IGNORE INTO {table_name} (modName, modAccess) VALUES ('{module_name}', 'other=-');"
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
2. `SELECT * FROM module_access` - Все права к модулям
3. `UPDATE module_access SET modAccess = 'NEWACCESS' WHERE modName = 'MODNAME'` - Задать новые права NEWACCESS для модуля MODNAME
'''

help_message = '''
📄 Существует БД для работы с правами
`module_access (modName, modAccess)` - содержит права для модулей

modAccess - строка
''' + user_access.user_access_readme

access_denied_message = '''
❌ Доступ запрещён!
''' 

access_button_name = "⛀ Доступ пользователей"
sql_request_button_name = "⛁ Запрос к БД для редактирования доступа"
help_button_name = "📄 Информация по редактированию доступа"

# ---------------------------------------------------------
# Работа с кнопками

def GetEditAccessKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(sql_request_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(help_button_name, user_access.AccessMode.VIEW, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# Приветствие
async def AccessStart(a_Message):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    if not user_access.CheckAccessString(GetAccess(), user_groups, user_access.AccessMode.VIEW):
        return await bot.send_message(user_id, access.access_denied_message, reply_markup = GetEditAccessKeyboardButtons(user_groups))
    await bot.send_message(user_id, access_start_message, reply_markup = GetEditAccessKeyboardButtons(user_groups))
# ---------------------------------------------------------
# Работа с базой данных 

def GetModuleAccessList():
    return bot_bd.SelectBDTemplate(table_name)()

def GetAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[1]
    return ''

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(access_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(AccessStart, text = access_button_name)

    dp.register_message_handler(groups.RequestToBDTemplate(request_start_message, GetAccess, FSMRequestToBD), text = sql_request_button_name)
    dp.register_message_handler(groups.RequestToBDCancelTemplate(GetEditAccessKeyboardButtons, GetAccess), text = groups.canсel_button_name, state = FSMRequestToBD.sqlRequest)
    dp.register_message_handler(groups.RequestToBDFinishTemplate(GetEditAccessKeyboardButtons, GetAccess), state = FSMRequestToBD.sqlRequest)

    dp.register_message_handler(groups.HelpTemplate(help_message, GetEditAccessKeyboardButtons, GetAccess), text = help_button_name)
