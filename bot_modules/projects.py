# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Проекты

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, access, groups
from template import bd_item_view, simple_message

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
    
class FSMEditProject(StatesGroup):
    prjID = State()
    prjPhoto = State()
    prjName = State()
    prjDesc = State()

# ---------------------------------------------------------
# БД
module_name = 'projects'

table_name = 'projects'
key_name = 'projectID'

init_bd_cmds = [f'''CREATE TABLE IF NOT EXISTS {table_name}(
    projectPhoto TEXT,
    projectName TEXT,
    projectDesc TEXT,
    projectAccess TEXT,
    {key_name} INTEGER PRIMARY KEY
)''',
f"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('{module_name}', 'other=va');"
]


# ---------------------------------------------------------
# Сообщения

base_project_message = '''
<b>🟥 Проекты</b>

'''
select_project_message = '''
Пожалуйста, выберите проект:
'''

error_find_proj_message = '''
❌ Ошибка, проект не найден
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

project_cancel_create_message = '🚫 Создание проекта отменено'

project_success_create_message = '✅ Проект успешно добавлен!'
project_success_delete_message = '✅ Проект успешно удалён!'
project_success_edit_message = '✅ Проект успешно отредактирован!'

project_create_message_0= '''
Редактирование проекта.

Пожалуйста, выберите проект:
'''

project_edit_message_1 = '''
Редактирование проекта. Шаг №1

Загрузите новую обложку для проекта (Фото):
Она будет отображаться в его описании.
'''

project_edit_message_2 = '''
Редактирование проекта. Шаг №2

Текущее название проекта:
@proj_name

Введите новое название проекта:
'''

project_edit_message_3 = '''
Редактирование проекта. Шаг №3

Текущее описание проекта:
@proj_desc

Введите новое описание проекта:
'''

project_cancel_edit_message = '🚫 Редактирование проекта отменено'

project_select_to_edit_message = '''
Выберите проект, который вы хотите отредактировать.
'''


project_select_to_delete_message = '''
Выберите проект, который вы хотите удалить.
Все задачи и потребности в этом проекте так же будут удалены!
'''

projects_button_name = "🟥 Проекты"
list_project_button_name = "📃 Список проектов"
add_project_button_name = "✅ Добавить проект"
del_project_button_name = "❌ Удалить проект"
edit_project_button_name = "🛠 Редактировать проект"
projects_canсel_button_name = "🚫 Отменить"
projects_skip_button_name = "⏩ Пропустить"


# Префиксы
select_project_callback_prefix = 'sel_project:'
delete_project_callback_prefix = 'del_project:'
select_to_edit_project_callback_prefix = 'sel_to_edit_project:'

# ---------------------------------------------------------
# Работа с кнопками

def GetEditProjectKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_project_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_project_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_project_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetCancelKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(projects_canсel_button_name, user_access.AccessMode.VIEW, GetAccess()),
    ]
    return keyboard.MakeKeyboard(cur_buttons, a_UserGroups)

def GetSkipAndCancelKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(projects_skip_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(projects_canсel_button_name, user_access.AccessMode.VIEW, GetAccess()),
    ]
    return keyboard.MakeKeyboard(cur_buttons, a_UserGroups)

def GetProjectsListKeyboardButtons(a_UserGroups, a_Prefix):
    projects = GetProjectList()
    projects_button_list = []
    for t in projects:
        projects_button_list += [keyboard.Button(str(t[1]), t[3])]
    return keyboard.MakeInlineKeyboard(projects_button_list, a_Prefix)

# ---------------------------------------------------------
# Обработка сообщений

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # projectName projectID projectAccess
    return a_Item[1], a_Item[4], a_Item[3]

async def ShowProject(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 3):
        return error_find_proj_message, None

    photo_id = a_Item[0]
    name =  a_Item[1]
    desc = a_Item[2]
    msg = project_open_message.replace('@proj_name', name).replace('@proj_desk', desc)
    return msg, photo_id

select_handler = 0
# стартовое сообщение
async def ProjectsOpen(a_Message : types.message):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await a_Message.answer(base_project_message, reply_markup = GetEditProjectKeyboardButtons(user_groups))
    await select_handler(a_Message)
    return None

# Создание нового проекта 
def GetProjectData(a_ProjectID):
    project = GetProject(a_ProjectID)
    if len(project) < 1:
        log.Error(f'Проект не найден {project_id}')
        msg = error_find_proj_message.replace('@project_id', project_id)
        return msg, '', '', ''

    p = project[0]
    return '', p[0], p[1], p[2]

async def ProjectCreateCancel(a_Message : types.message, state : FSMContext):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await state.finish()
    await a_Message.answer(project_cancel_create_message, reply_markup = GetEditProjectKeyboardButtons(user_groups))

async def ProjectCreate(a_Message : types.message):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await FSMCreateProject.prjPhoto.set()
    await a_Message.answer(project_create_message_1, reply_markup = GetSkipAndCancelKeyboardButtons(user_groups))

async def PhotoLoad(a_Message : types.message, state : FSMContext, a_FileID):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    async with state.proxy() as prjData:
        prjData['photo'] = a_FileID
    await FSMCreateProject.next()
    await a_Message.answer(project_create_message_2, reply_markup = GetCancelKeyboardButtons(user_groups))

async def ProjectPhotoLoad(a_Message : types.message, state : FSMContext):
    await PhotoLoad(a_Message, state, a_Message.photo[0].file_id)

async def ProjectPhotoSkip(a_Message : types.message, state : FSMContext):
    await PhotoLoad(a_Message, state, 0)

async def ProjectNameLoad(a_Message : types.message, state : FSMContext):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    async with state.proxy() as prjData:
        prjData['name'] = a_Message.text
    await FSMCreateProject.next()
    await a_Message.answer(project_create_message_3, reply_markup = GetCancelKeyboardButtons(user_groups))

async def ProjectDescLoad(a_Message : types.message, state : FSMContext):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    async with state.proxy() as prjData:
        prjData['desc'] = a_Message.text
        prjPhoto = prjData['photo']
        prjName = prjData['name']
        prjDesc = prjData['desc']
        AddProject(prjPhoto, prjName, prjDesc)
        log.Success(f'Добавлен проект {prjName} пользователем {a_Message.from_user.id}.')
    await state.finish()
    await a_Message.answer(project_success_create_message, reply_markup = GetEditProjectKeyboardButtons(user_groups))

# Редактирование проекта 

async def ProjectSelectForEdit(a_Message : types.message):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await bot.send_message(a_Message.from_user.id, project_select_to_edit_message, reply_markup = GetProjectsListKeyboardButtons(user_groups, select_to_edit_project_callback_prefix))

async def ProjectEditCancel(a_Message : types.message, state : FSMContext):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await state.finish()
    await a_Message.answer(project_cancel_edit_message, reply_markup = GetEditProjectKeyboardButtons(user_groups))

async def ProjectEdit(a_CallbackQuery : types.CallbackQuery, state : FSMContext):
    user_id = str(a_CallbackQuery.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await FSMEditProject.prjID.set()
    prjID = str(a_CallbackQuery.data).replace(select_to_edit_project_callback_prefix, '')
    async with state.proxy() as prjData:
        prjData['prjID'] = prjID
    await FSMEditProject.next()
    await bot.send_message(a_CallbackQuery.from_user.id, project_edit_message_1, reply_markup = GetSkipAndCancelKeyboardButtons(user_groups))

async def PhotoEditLoad(a_Message : types.message, state : FSMContext, a_FileID):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    project_id = 0
    async with state.proxy() as prjData:
        prjData['photo'] = a_FileID
        project_id = prjData['prjID']
    await FSMEditProject.next()
    msg, photo_id, name, desc = GetProjectData(project_id)
    if msg != '':
        await bot.send_message(a_Message.from_user.id, msg, reply_markup = GetEditProjectKeyboardButtons(user_groups))
        return
    await a_Message.answer(project_edit_message_2.replace('@proj_name', name), reply_markup = GetSkipAndCancelKeyboardButtons(user_groups))

async def ProjectEditPhotoLoad(a_Message : types.message, state : FSMContext):
    await PhotoEditLoad(a_Message, state, a_Message.photo[0].file_id)

async def ProjectEditPhotoSkip(a_Message : types.message, state : FSMContext):
    project_id = 0
    async with state.proxy() as prjData:
        project_id = prjData['prjID']
    msg, photo_id, name, desc = GetProjectData(project_id)
    if msg != '':
        await bot.send_message(a_Message.from_user.id, msg, reply_markup = GetEditProjectKeyboardButtons(user_groups))
        return
    await PhotoEditLoad(a_Message, state, photo_id)

async def EditNameSkip(a_Message : types.message, state : FSMContext, a_Name):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    async with state.proxy() as prjData:
        prjData['name'] = a_Name
    await FSMEditProject.next()
    await a_Message.answer(project_edit_message_3, reply_markup = GetSkipAndCancelKeyboardButtons(user_groups))

async def ProjectEditNameLoad(a_Message : types.message, state : FSMContext):
    await EditNameSkip(a_Message, state, a_Message.text)

async def ProjectEditDescLoad(a_Message : types.message, state : FSMContext):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    async with state.proxy() as prjData:
        prjData['desc'] = a_Message.text
        project_id = prjData['prjID']
        prjPhoto = prjData['photo']
        prjName = prjData['name']
        prjDesc = prjData['desc']
        EditProject(project_id, prjPhoto, prjName, prjDesc)
        log.Success(f'Изменён проект {prjName} пользователем {a_Message.from_user.id}.')
    await state.finish()
    await a_Message.answer(project_success_edit_message, reply_markup = GetEditProjectKeyboardButtons(user_groups))

# Удаление проекта 

async def ProjectDelete(a_Message : types.message):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await bot.send_message(a_Message.from_user.id, project_select_to_delete_message, reply_markup = GetProjectsListKeyboardButtons(user_groups, delete_project_callback_prefix))

async def prjDelete(a_CallbackQuery : types.CallbackQuery):
    user_id = str(a_CallbackQuery.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    projectID = str(a_CallbackQuery.data).replace(delete_project_callback_prefix, '')
    DelProject(projectID)
    log.Success(f'Проект №{projectID} был удалён пользователем {a_CallbackQuery.from_user.id}.')
    await bot.send_message(a_CallbackQuery.from_user.id, project_success_delete_message, reply_markup = GetEditProjectKeyboardButtons(user_groups))

# ---------------------------------------------------------
# Работа с базой данных проектов

def GetProjectList():
    return bot_bd.SelectBDTemplate(table_name)()

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

def EditProject(a_ProjectID, a_prjPhoto, a_prjName, a_prjDesc):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    cursor.execute('UPDATE projects SET projectPhoto = ?, projectName = ?, projectDesc = ? WHERE projectID = ?', (a_prjPhoto, a_prjName, a_prjDesc, a_ProjectID))
    db.commit()
    cursor.close()
    db.close()
    return

def DelProject(a_ProjectID):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    cursor.execute('DELETE FROM projects WHERE projectID = ?', ([a_ProjectID]))
    db.commit()
    db.close()
    return

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(projects_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(simple_message.SimpleMessageTemplate(ProjectsOpen, GetEditProjectKeyboardButtons, GetAccess), text = projects_button_name)

    global select_handler
    select_handler = bd_item_view.SelectAndShowBDItemRegisterHandlers(dp, list_project_button_name, table_name, key_name, ShowProject, GetButtonNameAndKeyValueAndAccess, select_project_message, GetAccess, GetEditProjectKeyboardButtons)

# Добавление проекта
    dp.register_message_handler(ProjectCreate, text = add_project_button_name)
    dp.register_message_handler(ProjectPhotoSkip, text = projects_skip_button_name, state = FSMCreateProject.prjPhoto)
    dp.register_message_handler(ProjectCreateCancel, text = projects_canсel_button_name, state = FSMCreateProject.prjPhoto)
    dp.register_message_handler(ProjectCreateCancel, text = projects_canсel_button_name, state = FSMCreateProject.prjName)
    dp.register_message_handler(ProjectCreateCancel, text = projects_canсel_button_name, state = FSMCreateProject.prjDesc)
    dp.register_message_handler(ProjectPhotoLoad, content_types = ['photo'], state = FSMCreateProject.prjPhoto)
    dp.register_message_handler(ProjectNameLoad, state = FSMCreateProject.prjName)
    dp.register_message_handler(ProjectDescLoad, state = FSMCreateProject.prjDesc)
# Редактирование проекта
    dp.register_message_handler(ProjectSelectForEdit, text = edit_project_button_name)
    dp.register_callback_query_handler(ProjectEdit, lambda x: x.data.startswith(select_to_edit_project_callback_prefix))
    dp.register_message_handler(ProjectEditPhotoSkip, text = projects_skip_button_name, state = FSMEditProject.prjPhoto)
    dp.register_message_handler(ProjectEditCancel, text = projects_canсel_button_name, state = FSMEditProject.prjPhoto)
    dp.register_message_handler(ProjectEditCancel, text = projects_canсel_button_name, state = FSMEditProject.prjName)
    dp.register_message_handler(ProjectEditCancel, text = projects_canсel_button_name, state = FSMEditProject.prjDesc)
    dp.register_message_handler(ProjectEditPhotoLoad, content_types = ['photo'], state = FSMEditProject.prjPhoto)
    dp.register_message_handler(ProjectEditNameLoad, state = FSMEditProject.prjName)
    dp.register_message_handler(ProjectEditDescLoad, state = FSMEditProject.prjDesc)
# Удаление проекта
    dp.register_message_handler(ProjectDelete, text = del_project_button_name)
    dp.register_callback_query_handler(prjDelete, lambda x: x.data.startswith(delete_project_callback_prefix))
