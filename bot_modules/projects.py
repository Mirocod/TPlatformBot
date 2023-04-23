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

base_project_message = '''
<b>🛒 Проекты</b>

'''
select_project_message = '''
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
add_project_button_name = "📰 Добавить проект"
del_project_button_name = "📰 Удалить проект"
edit_project_button_name = "📰 Редактировать проект"

# Префиксы
select_project_callback_prefix = 'project:'

# ---------------------------------------------------------
# Работа с кнопками

def GetEditProjectKeyboardButtons(a_UserAccess, a_ParentID):
    proj_buttons = [add_project_button_name, del_project_button_name, edit_project_button_name]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods, a_UserAccess) + proj_buttons)

def GetProjectsListKeyboardButtons(a_UserAccess, a_ParentID):
    projects = GetProjectList(a_ParentID)
    projects_button_list = []
    for t in projects:
        projects_button_list += [keyboard.Button(str(t[1]), t[4])]
    return keyboard.MakeInlineKeyboard(projects_button_list, select_project_callback_prefix)

def GetUserAccess(a_UserID):
    return None

# ---------------------------------------------------------
# Обработка сообщений

# Отображение всех проектов без родителя
async def ProjectsOpen(a_Message, **kwargs):
    print('test', kwargs)
    user_access = GetUserAccess(a_Message.from_user.id)
    await bot.send_message(a_Message.from_user.id, base_project_message, reply_markup = GetEditProjectKeyboardButtons(user_access, 0))
    await bot.send_message(a_Message.from_user.id, select_project_message, reply_markup = GetProjectsListKeyboardButtons(user_access, 0))

async def ShowProject(a_CallbackQuery : types.CallbackQuery):
    project_id = str(a_CallbackQuery.data).replace(select_project_callback_prefix, '')
    user_access = GetUserAccess(a_CallbackQuery.from_user.id)
    project = GetProject(project_id)
    if len(project) != 1:
        log.Error(f'Проект не найден {project_id}')
        msg = Ошибка.replace('@project_id', project_id)
        await bot.send_message(a_CallbackQuery.from_user.id, msg, reply_markup = GetEditProjectKeyboardButtons(user_access, project_id))
        return

    p = project[0]
    msg = project_open_message.replace('@proj_name', p[1]).replace('@proj_desk', p[2])
    await bot.send_photo(a_CallbackQuery.from_user.id, p[0], msg, reply_markup = GetEditProjectKeyboardButtons(user_access, project_id))

# ---------------------------------------------------------
# Работа с базой данных проектов

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
    project = cursor.execute('SELECT * FROM projects WHERE projectID = ?', ([a_ProjectID])).fetchall()
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
'''
    dp.register_message_handler(ProjectCreate, text = add_project_button_name)
    dp.register_message_handler(ProjectDelete, text = del_project_button_name)
    dp.register_callback_query_handler(catDelete, lambda x: x.data.startswith('delcat '))
    dp.register_message_handler(ProjectPhotoLoad, content_types = ['photo'], state = FSMCreateCategory.catPhoto)
    dp.register_message_handler(ProjectNameLoad, state = FSMCreateCategory.catName)
    dp.register_message_handler(ProjectDescLoad, state = FSMCreateCategory.catDesc)'''
