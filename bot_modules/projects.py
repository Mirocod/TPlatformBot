# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Проекты

from bot_sys import bot_bd, log, keyboard, user_access
from bot_modules import start, access, groups
from template import bd_item_view, simple_message, bd_item_delete, bd_item_edit, bd_item, bd_item_add

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

class FSMCreateProject(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditPhotoItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditNameItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditDeskItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditAccessItem(StatesGroup):
    item_id = State()
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'projects'

table_name = module_name
key_name = 'projectID'
name_field = 'projectName'
desc_field = 'projectDesc'
photo_field = 'projectPhoto'
access_field = 'projectAccess'
create_datetime_field = 'projectCreateDateTime'

init_bd_cmds = [f'''CREATE TABLE IF NOT EXISTS {table_name}(
    {key_name} INTEGER PRIMARY KEY,
    {name_field} TEXT,
    {desc_field} TEXT,
    {photo_field} TEXT,
    {access_field} TEXT,
    {create_datetime_field} TEXT
    )''',
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_new}=va', '{user_access.user_access_group_new}=va');"
]

# ---------------------------------------------------------
# Сообщения

projects_button_name = "🟥 Проекты"
base_project_message = '''
<b>🟥 Проекты</b>

'''

list_project_button_name = "📃 Список проектов"
select_project_message = '''
Пожалуйста, выберите проект:
'''

error_find_proj_message = '''
❌ Ошибка, проект не найден
'''

project_open_message = f'''
<b>Проект:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
'''

# Создание проекта

add_project_button_name = "✅ Добавить проект"
project_create_name_message = '''
Создание проекта. Шаг №1

Введите название проекта:
'''

project_create_desc_message = '''
Создание проекта. Шаг №2

Введите описание проекта:
'''

project_create_photo_message = '''
Создание проекта. Шаг №3

Загрузите обложку для проекта (Фото):
Она будет отображаться в его описании.
'''

project_success_create_message = '''✅ Проект успешно добавлен!'''

# Редактирование проекта.

edit_project_button_name = "🛠 Редактировать проект"
project_start_edit_message= '''
Пожалуйста, выберите действие:
'''

project_select_to_edit_message = '''
Выберите проект, который вы хотите отредактировать.
'''

edit_project_photo_button_name = "☐ Изменить изображение"
project_edit_photo_message = '''
Загрузите новую обложку для проекта (Фото):
Она будет отображаться в его описании.
'''

edit_project_name_button_name = "≂ Изменить название"
project_edit_name_message = f'''
Текущее название проекта:
#{name_field}

Введите новое название проекта:
'''

edit_project_desc_button_name = "𝌴 Изменить описание"
project_edit_desc_message = f'''
Текущее описание проекта:
#{desc_field}

Введите новое описание проекта:
'''

edit_project_access_button_name = "✋ Изменить доступ"
project_edit_access_message = f'''
Текущий доступ к проекту:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

project_success_edit_message = '''✅ Проект успешно отредактирован!'''

# Удаление проекта

del_project_button_name = "❌ Удалить проект"
project_select_to_delete_message = '''
Выберите проект, который вы хотите удалить.
Все задачи и потребности в этом проекте так же будут удалены!
'''

project_success_delete_message = '''✅ Проект успешно удалён!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditProjectKeyboardButtons(a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_project_photo_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_name_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartProjectKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_project_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_project_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_project_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

select_handler = 0
# стартовое сообщение
async def ProjectsOpen(a_Message : types.message, state = None):
    user_id = str(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    await a_Message.answer(base_project_message, reply_markup = GetStartProjectKeyboardButtons(user_groups))
    await select_handler(a_Message)
    return None

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # projectName projectID projectAccess
    return a_Item[1], a_Item[0], a_Item[4]

def ShowMessageTemplate(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 6):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = a_StringMessage.\
                replace(f'#{name_field}', a_Item[1]).\
                replace(f'#{desc_field}', a_Item[2]).\
                replace(f'#{create_datetime_field}', a_Item[5]).\
                replace(f'#{access_field}', a_Item[4])
        return simple_message.WorkFuncResult(msg, photo_id = a_Item[3], item_access = a_Item[4])
    return ShowMessage

def SimpleMessageTemplate(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery):
        return simple_message.WorkFuncResult(a_StringMessage)
    return ShowMessage

# Удаление проекта 

async def ProjectPreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 6):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[4]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def ProjectPostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Проект №{a_ItemID} был удалён пользователем {a_CallbackQuery.from_user.id}.')
    return simple_message.WorkFuncResult(project_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных проектов

def AddBDItemFunc(a_ItemData):
    res, error = bot_bd.SQLRequestToBD(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], access.GetItemDefaultAccessForModule(module_name)))

    if error:
        log.Error(f'Ошибка добавления записи в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')
    else:
        log.Success(f'Добавлена запись в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')

    return res, error

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

    # Список проектов
    dp.register_message_handler(simple_message.SimpleMessageTemplate(ProjectsOpen, GetStartProjectKeyboardButtons, GetAccess), text = projects_button_name)
    global select_handler
    select_handler = bd_item_view.SelectAndShowBDItemRegisterHandlers(dp, list_project_button_name, table_name, key_name, ShowMessageTemplate(project_open_message), GetButtonNameAndKeyValueAndAccess, select_project_message, GetAccess, GetStartProjectKeyboardButtons)

    # Удаление проекта
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, del_project_button_name, table_name, key_name, ProjectPreDelete, ProjectPostDelete, GetButtonNameAndKeyValueAndAccess, select_project_message, GetAccess, GetStartProjectKeyboardButtons)

    # Добавление проекта
    bd_item_add.AddBDItem3RegisterHandlers(dp, FSMCreateProject, FSMCreateProject.name, FSMCreateProject.desc, FSMCreateProject.photo, add_project_button_name, AddBDItemFunc, SimpleMessageTemplate(project_create_name_message), SimpleMessageTemplate(project_create_desc_message), SimpleMessageTemplate(project_create_photo_message), SimpleMessageTemplate(project_success_create_message), table_name, key_name, name_field, desc_field, photo_field, GetButtonNameAndKeyValueAndAccess, GetAccess, GetStartProjectKeyboardButtons)

    # Редактирование проекта
    dp.register_message_handler(simple_message.InfoMessageTemplate(project_start_edit_message, GetEditProjectKeyboardButtons, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_project_button_name)
    bd_item_edit.EditBDItemRegisterHandlers(dp, FSMEditPhotoItem, edit_project_photo_button_name, project_select_to_edit_message, ShowMessageTemplate(project_edit_photo_message), ShowMessageTemplate(project_success_edit_message), table_name, key_name, photo_field, GetButtonNameAndKeyValueAndAccess, GetAccess, GetEditProjectKeyboardButtons, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.photo)
    bd_item_edit.EditBDItemRegisterHandlers(dp, FSMEditNameItem, edit_project_name_button_name, project_select_to_edit_message, ShowMessageTemplate(project_edit_name_message), ShowMessageTemplate(project_success_edit_message), table_name, key_name, name_field, GetButtonNameAndKeyValueAndAccess, GetAccess, GetEditProjectKeyboardButtons, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.text)
    bd_item_edit.EditBDItemRegisterHandlers(dp, FSMEditDeskItem, edit_project_desc_button_name, project_select_to_edit_message, ShowMessageTemplate(project_edit_desc_message), ShowMessageTemplate(project_success_edit_message), table_name, key_name, desc_field, GetButtonNameAndKeyValueAndAccess, GetAccess, GetEditProjectKeyboardButtons, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.text)
    bd_item_edit.EditBDItemRegisterHandlers(dp, FSMEditAccessItem, edit_project_access_button_name, project_select_to_edit_message, ShowMessageTemplate(project_edit_access_message), ShowMessageTemplate(project_success_edit_message), table_name, key_name, access_field, GetButtonNameAndKeyValueAndAccess, GetAccess, GetEditProjectKeyboardButtons, access_mode = user_access.AccessMode.ACCEES_EDIT, field_type = bd_item.FieldType.text)

