# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Проекты

from bot_sys import bot_bd, log, config, keyboard
from bot_modules import start
from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
init_bd_cmd = '''CREATE TABLE IF NOT EXISTS projects(
    projectPhoto TEXT,
    projectName TEXT,
    projectDesc TEXT,
    parentID INTEGER,
    projectID INTEGER PRIMARY KEY
)'''

# ---------------------------------------------------------
# Сообщения

select_project_message = '''
<b>🛒 Проекты</b>

Пожалуйста, выберите проект:
'''

error_find_proj_message = '''
Ошибка, проект с ID @project_id не найден
'''

project_open_message = '''
<b>Проект:  @proj_name</b>

@proj_desk
'''

projects_button_name = "📰 Проекты"

# Префиксы
select_project_callback_prefix = 'project:'

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons(a_UserAccess):
    mods = [start]
    return keyboard.MakeKeyboardForMods(mods, a_UserAccess)

# ---------------------------------------------------------
# Обработка сообщений

# Отображение всех проектов без родителя
async def ProjectsOpen(a_Message):
    projects = GetProjectList(0)
    projects_button_list = []
    for t in projects:
        b = keyboard.Button(str(t[1]), t[4])
    await bot.send_message(a_Message.from_user.id, select_project_message, reply_markup=keyboard.MakeInlineKeyboard(projects_button_list, select_project_callback_prefix))

async def ShowProject(a_CallbackQuery : types.CallbackQuery):
    project_id = str(a_CallbackQuery.data).replace(select_project_callback_prefix, '')
    project = GetProject(project_id)
    if len(project) != 1:
        log.Error(f'Проект не найден {project_id}')
        msg = Ошибка.replace('@project_id', project_id)
        await bot.send_message(a_CallbackQuery.from_user.id, msg, reply_markup=keyboard.MakeKeyboardForMods([start]))
        return

    p = project[0]
    msg = project_open_message.replace('@proj_name', p[1]).replace('@proj_desk', p[2])
    await bot.send_photo(a_CallbackQuery.from_user.id, p[0], msg, reply_markup=keyboard.MakeKeyboardForMods([start]))

# ---------------------------------------------------------
# Работа с базой данных пользователей

def GetProjectList(a_ParentID):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    projects = cursor.execute('SELECT * FROM projects where parentID = ?', ([a_ParentID])).fetchall()
    cursor.close()
    db.close()
    return projects

def GetProject(a_ProjectID):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    project = cursor.execute('SELECT * FROM categories WHERE catID = ?', ([catID])).fetchall()
    cursor.close()
    db.close()
    return project

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return [init_bd_cmd]

# Доступные кнопки
def GetButtonNames(a_UserAccess):
    return [projects_button_name]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(ProjectsOpen, text = projects_button_name)
    dp.register_callback_query_handler(ShowProject, lambda x: x.data.startswith(select_project_callback_prefix))
