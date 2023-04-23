# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Проекты

from bot_sys import bot_bd, log, config, keyboard
from bot_modules import start
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode = types.ParseMode.HTML)

class FSMCreateProject(StatesGroup):
    prjPhoto = State()
    prjName = State()
    prjDesc = State()

# ---------------------------------------------------------
# БД
init_bd_cmd = '''CREATE TABLE IF NOT EXISTS projects(
    projectPhoto TEXT,
    projectName TEXT,
    projectDesc TEXT,
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

project_create_message_1 = '''
Создание проекта. Шаг №1

Загрузите обложку для проекта (Фото):
Она будет отображаться в его описании.
'''

project_create_message_2 = '''
Создание проекта. Шаг №2

Введите название проекта:
'''

project_create_message_3 = '''
Создание проекта. Шаг №3

Введите описание проекта:
'''

project_success_create_message = 'Проект успешно добавлен!'
project_success_delete_message = 'Проект успешно удалён!'

project_cancel_create_message = 'Действие отменено'


project_select_to_delete_message = '''
Выберите проект, который вы хотите удалить.
Все задачи и потребности в этом проекте так же будут удалены!
'''

projects_button_name = "📰 Проекты"
add_project_button_name = "📰 Добавить проект"
del_project_button_name = "📰 Удалить проект"
edit_project_button_name = "📰 Редактировать проект"
projects_canсel_button_name = "📰 Отменить"


# Префиксы
select_project_callback_prefix = 'sel_project:'
delete_project_callback_prefix = 'del_project:'


# ---------------------------------------------------------
# Работа с кнопками

def GetEditProjectKeyboardButtons(a_UserAccess):
    proj_buttons = [add_project_button_name, del_project_button_name, edit_project_button_name]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods, a_UserAccess) + proj_buttons)

def GetCancelKeyboardButtons(a_UserAccess):
#    return keyboard.MakeKeyboardRemove()
    return keyboard.MakeKeyboard([projects_canсel_button_name])

def GetProjectsListKeyboardButtons(a_UserAccess, a_Prefix):
    projects = GetProjectList()
    projects_button_list = []
    for t in projects:
        projects_button_list += [keyboard.Button(str(t[1]), t[3])]
    return keyboard.MakeInlineKeyboard(projects_button_list, a_Prefix)

def GetUserAccess(a_UserID):
    return None

# ---------------------------------------------------------
# Обработка сообщений

# Отображение всех проектов без родителя
async def ProjectsOpen(a_Message : types.message):
    user_access = GetUserAccess(a_Message.from_user.id)
    await bot.send_message(a_Message.from_user.id, base_project_message, reply_markup = GetEditProjectKeyboardButtons(user_access))
    await bot.send_message(a_Message.from_user.id, select_project_message, reply_markup = GetProjectsListKeyboardButtons(user_access, select_project_callback_prefix))

async def ShowProject(a_CallbackQuery : types.CallbackQuery):
    project_id = str(a_CallbackQuery.data).replace(select_project_callback_prefix, '')
    user_access = GetUserAccess(a_CallbackQuery.from_user.id)
    project = GetProject(project_id)
    if len(project) != 1:
        log.Error(f'Проект не найден {project_id}')
        msg = Ошибка.replace('@project_id', project_id)
        await bot.send_message(a_CallbackQuery.from_user.id, msg, reply_markup = GetEditProjectKeyboardButtons(user_access))
        return

    p = project[0]
    msg = project_open_message.replace('@proj_name', p[1]).replace('@proj_desk', p[2])
    await bot.send_photo(a_CallbackQuery.from_user.id, p[0], msg, reply_markup = GetEditProjectKeyboardButtons(user_access))

async def ProjectCreateCancel(a_Message : types.message, state : FSMContext):
    user_access = GetUserAccess(a_Message.from_user.id)
    await state.finish()
    await a_Message.answer(project_cancel_create_message, reply_markup = GetEditProjectKeyboardButtons(user_access))

async def ProjectCreate(a_Message : types.message):
    user_access = GetUserAccess(a_Message.from_user.id)
    await FSMCreateProject.prjPhoto.set()
    await a_Message.answer(project_create_message_1, reply_markup = GetCancelKeyboardButtons(user_access))

async def ProjectPhotoLoad(a_Message : types.message, state : FSMContext):
    user_access = GetUserAccess(a_Message.from_user.id)
    async with state.proxy() as prjData:
        prjData['photo'] = a_Message.photo[0].file_id
    await FSMCreateProject.next()
    await a_Message.answer(project_create_message_2, reply_markup = GetCancelKeyboardButtons(user_access))

async def ProjectNameLoad(a_Message : types.message, state : FSMContext):
    user_access = GetUserAccess(a_Message.from_user.id)
    async with state.proxy() as prjData:
        prjData['name'] = a_Message.text
        await FSMCreateProject.next()
        await a_Message.answer(project_create_message_3, reply_markup = GetCancelKeyboardButtons(user_access))

async def ProjectDescLoad(a_Message : types.message, state : FSMContext):
    user_access = GetUserAccess(a_Message.from_user.id)
    async with state.proxy() as prjData:
        prjData['desc'] = a_Message.text
        prjPhoto = prjData['photo']
        prjName = prjData['name']
        prjDesc = prjData['desc']
        AddProject(prjPhoto, prjName, prjDesc)
        log.Success(f'Добавлен проект {prjName} пользователем {a_Message.from_user.id}.')
    await state.finish()
    await a_Message.answer(project_success_create_message, reply_markup = GetEditProjectKeyboardButtons(user_access))

async def ProjectDelete(a_Message : types.message):
    user_access = GetUserAccess(a_Message.from_user.id)
    await bot.send_message(a_Message.from_user.id, project_select_to_delete_message, reply_markup = GetProjectsListKeyboardButtons(user_access, delete_project_callback_prefix))

async def prjDelete(a_CallbackQuery : types.CallbackQuery):
    user_access = GetUserAccess(a_CallbackQuery.from_user.id)
    projectID = str(a_CallbackQuery.data).replace(delete_project_callback_prefix, '')
    DelProject(projectID)
    log.Success(f'Проект №{projectID} был удален пользователем {a_CallbackQuery.from_user.id}.')
    await bot.send_message(a_CallbackQuery.from_user.id, project_success_delete_message, reply_markup = GetEditProjectKeyboardButtons(user_access))

# ---------------------------------------------------------
# Работа с базой данных проектов

def GetProjectList():
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    projects = cursor.execute('SELECT * FROM projects').fetchall()
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

def AddProject(a_prjPhoto, a_prjName, a_prjDesc):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    cursor.execute('INSERT INTO projects(projectPhoto, projectName, projectDesc) VALUES(?, ?, ?)', (a_prjPhoto, a_prjName, a_prjDesc))
    db.commit()
    cursor.close()
    db.close()
    return

def DelProject(a_ProjectID):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    cursor.execute('DELETE FROM projects WHERE projectID = ?', ([a_ProjectID]))
    #cursor.execute('DELETE FROM tasks WHERE projectID = ?', ([a_ProjectID]))
    db.commit()
    db.close()
    return

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
    dp.register_message_handler(ProjectCreate, text = add_project_button_name)
    dp.register_message_handler(ProjectCreateCancel, text = projects_canсel_button_name, state = FSMCreateProject.prjPhoto)
    dp.register_message_handler(ProjectCreateCancel, text = projects_canсel_button_name, state = FSMCreateProject.prjName)
    dp.register_message_handler(ProjectCreateCancel, text = projects_canсel_button_name, state = FSMCreateProject.prjDesc)
    dp.register_message_handler(ProjectPhotoLoad, content_types = ['photo'], state = FSMCreateProject.prjPhoto)
    dp.register_message_handler(ProjectNameLoad, state = FSMCreateProject.prjName)
    dp.register_message_handler(ProjectDescLoad, state = FSMCreateProject.prjDesc)
    dp.register_message_handler(ProjectDelete, text = del_project_button_name)
    dp.register_callback_query_handler(prjDelete, lambda x: x.data.startswith(delete_project_callback_prefix))
