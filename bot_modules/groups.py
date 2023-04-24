# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы пользователей

from bot_sys import bot_bd, log, config, keyboard
from bot_modules import start, access
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
"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('groups', 'other=-');"
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
Существует две БД для работы с группами
`user_groups (group_id, groupName)` - содержит названия групп
`user_in_groups(user_id, group_id)` - содержит соответсвия ID пользователей и групп
 '''

request_cancel_message = '''
Запрос к БД отменён
'''

user_group_button_name = "📰 Группы пользователей"
sql_request_button_name = "📰 Запрос к БД для редактирования групп"
help_button_name = "📰 Информация по группам"
canсel_button_name = "📰 Отменить"

# ---------------------------------------------------------
# Работа с кнопками

def GetEditGroupKeyboardButtons(a_UserAccess):
    cur_buttons = [sql_request_button_name, help_button_name]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods, a_UserAccess) + cur_buttons)

def GetCancelKeyboardButtons(a_UserAccess):
    return keyboard.MakeKeyboard([canсel_button_name])

# ---------------------------------------------------------
# Обработка сообщений

# Приветствие
async def GroupStart(a_Message):
    user_id = str(a_Message.from_user.id)
    user_access = access.GetUserAccess(a_Message.from_user.id)
    await bot.send_message(user_id, group_start_message, reply_markup = GetEditGroupKeyboardButtons(user_access))

async def RequestToBDCancel(a_Message : types.message, state : FSMContext):
    user_access = access.GetUserAccess(a_Message.from_user.id)
    await state.finish()
    await a_Message.answer(request_cancel_message, reply_markup = GetEditGroupKeyboardButtons(user_access))

def HelpTemplate(a_HelpMessage, a_GetButtonsFunc):
    async def Help(a_Message : types.message):
        user_access = access.GetUserAccess(a_Message.from_user.id)
        await a_Message.answer(a_HelpMessage, reply_markup = a_GetButtonsFunc(user_access)) #, parse_mode='Markdown')
    return Help

def RequestToBDTemplate(a_StartMessage):
    async def RequestToBDStart(a_Message : types.message):
        user_access = access.GetUserAccess(a_Message.from_user.id)
        await FSMRequestToBD.sqlRequest.set()
        await a_Message.answer(a_StartMessage, reply_markup = GetCancelKeyboardButtons(user_access), parse_mode='Markdown')
    return RequestToBDStart

async def RequestToBD(a_Message : types.message, state : FSMContext):
    user_access = access.GetUserAccess(a_Message.from_user.id)
    result = ''
    async with state.proxy() as prjData:
        sql_request = a_Message.text
        log.Success(f'Сделан запрос [{sql_request}] пользователем {a_Message.from_user.id}.')
        result = bot_bd.SQLRequestToBDCommit(sql_request)
        log.Success(f'Результат запроса [{sql_request}] от пользователя {a_Message.from_user.id} следующий [{result}].')
    await state.finish()
    await a_Message.answer(str(result), reply_markup = GetEditGroupKeyboardButtons(user_access))

# ---------------------------------------------------------
# Работа с базой данных групп

def GetGroupIDForUser(a_UserID):
    return bot_bd.SQLRequestToBD1('SELECT group_id FROM user_in_groups WHERE user_id = ?', a_UserID)

def GetGroupNamesForUser(a_UserID):
    return bot_bd.SQLRequestToBD1('SELECT groupName FROM user_groups WHERE group_id=(SELECT group_id FROM user_in_groups WHERE user_id = ?)', a_UserID)

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

# Доступные кнопки
def GetButtonNames(a_UserAccess):
    return [user_group_button_name]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(GroupStart, text = user_group_button_name)
    dp.register_message_handler(RequestToBDTemplate(request_start_message), text = sql_request_button_name)
    dp.register_message_handler(HelpTemplate(help_message, GetEditGroupKeyboardButtons), text = help_button_name)
    dp.register_message_handler(RequestToBDCancel, text = canсel_button_name, state = FSMRequestToBD.sqlRequest)
    dp.register_message_handler(RequestToBD, state = FSMRequestToBD.sqlRequest)
