# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, groups
from template import simple_message, sql_request

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher

class FSMRequestToBDAccess(StatesGroup):
    sqlRequest = State()

# ---------------------------------------------------------
# БД
table_name = 'module_access'
module_name = 'access'

init_bd_cmds = [f"""CREATE TABLE IF NOT EXISTS {table_name}(
    modName TEXT,
    modAccess TEXT,
    itemDefaultAccess TEXT,
    UNIQUE(modName)
);""",
f"INSERT OR IGNORE INTO {table_name} (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_all}=-', '{user_access.user_access_group_all}=-');"
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
        keyboard.ButtonWithAccess(sql_request_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(help_button_name, user_access.AccessMode.VIEW, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# ---------------------------------------------------------
# Работа с базой данных 

def GetModuleAccessList():
    return bot_bd.SelectBDTemplate(table_name)()

# ---------------------------------------------------------
# API

def GetAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[1]
    return ''

def GetItemDefaultAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[2]
    return ''

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
    dp.register_message_handler(simple_message.InfoMessageTemplate(access_start_message, GetEditAccessKeyboardButtons, GetAccess), text = access_button_name)
    dp.register_message_handler(simple_message.InfoMessageTemplate(help_message, GetEditAccessKeyboardButtons, GetAccess), text = help_button_name)

    sql_request.RequestToBDRegisterHandlers(dp, sql_request_button_name, request_start_message, FSMRequestToBDAccess, GetEditAccessKeyboardButtons, user_access.AccessMode.ACCEES_EDIT, GetAccess)
