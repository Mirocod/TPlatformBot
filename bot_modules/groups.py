# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы пользователей

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, access
from template import simple_message, sql_request

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher

class FSMRequestToBD(StatesGroup):
    sqlRequest = State()

# ---------------------------------------------------------
# БД
module_name = 'groups'

init_bd_cmds = ["""CREATE TABLE IF NOT EXISTS user_groups(
    group_id INTEGER PRIMARY KEY NOT NULL,
    groupName TEXT,
    UNIQUE(group_id)
);""",
"""CREATE TABLE IF NOT EXISTS user_in_groups(
    user_id INTEGER,
    group_id INTEGER,
    UNIQUE(user_id, group_id)
);""",
f"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('{module_name}', 'other=-');"
]

# ---------------------------------------------------------
# Сообщения

group_start_message = '''
<b>Группы пользователей находятся в стадии разработки</b>

Пока можете воспользоваться хардкорным способом через запросы к БД
'''

request_start_message = '''
**Задайте запрос к БД**

Можете воспользоваться следующими шаблонами:
1. `SELECT * FROM users` - Все пользователи
2. `SELECT group_id, groupName FROM user_groups` - Все группы пользоватлей
3. `INSERT INTO user_groups(groupName) VALUES('GROUPNAME')` - добавление группы с именем GROUPNAME
4. `SELECT group_id FROM user_in_groups WHERE user_id = USERID`- Все ID групп в которых состоит пользователь с USERID
5. `SELECT groupName FROM user_groups WHERE group_id=(SELECT groupid FROM user_in_groups WHERE user_id = USERID)` - Все имена групп пользователя с USERID
6. `INSERT INTO user_in_groups(user_id, group_id) VALUES(USERID, GROUPID)` - добавление пользователя USERID в группу с GROUPID
'''

help_message = '''
📄 Существует две БД для работы с группами
`user_groups (group_id, groupName)` - содержит названия групп
`user_in_groups(user_id, group_id)` - содержит соответсвия ID пользователей и групп
 '''

request_cancel_message = '''
Запрос к БД отменён
'''

user_group_button_name = "‍️️▦ Группы пользователей"
sql_request_button_name = "⛃ Запрос к БД для редактирования групп"
help_button_name = "📄 Информация по группам"

# ---------------------------------------------------------
# Работа с кнопками

def GetEditGroupKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(sql_request_button_name, user_access.AccessMode.EDIT, GetAccess()), 
        keyboard.ButtonWithAccess(help_button_name, user_access.AccessMode.VIEW, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# ---------------------------------------------------------
# Работа с базой данных групп

def GetGroupIDForUser(a_UserID):
    return bot_bd.SQLRequestToBD('SELECT group_id FROM user_in_groups WHERE user_id = ?', param = [a_UserID])

def GetGroupNamesForUser(a_UserID):
    return bot_bd.SQLRequestToBD('SELECT groupName FROM user_groups WHERE group_id=(SELECT group_id FROM user_in_groups WHERE user_id = ?)', param = [a_UserID])

# ---------------------------------------------------------
# API

def GetUserGroupData(a_UserID):
    r = GetGroupNamesForUser(a_UserID)
    groups = []
    for i in r:
        if len(i) > 0:
            groups += [i[0]]
    return user_access.UserGroups(a_UserID, groups)

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(user_group_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(simple_message.InfoMessageTemplate(group_start_message, GetEditGroupKeyboardButtons, GetAccess), text = user_group_button_name)
    dp.register_message_handler(simple_message.InfoMessageTemplate(help_message, GetEditGroupKeyboardButtons, GetAccess), text = help_button_name)

    sql_request.RequestToBDRegisterHandlers(dp, sql_request_button_name, request_start_message, FSMRequestToBD, GetEditGroupKeyboardButtons, user_access.AccessMode.EDIT, GetAccess)
