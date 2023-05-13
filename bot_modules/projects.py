# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Проекты

from bot_sys import bot_bd, log, keyboard, user_access, user_messages
from bot_modules import start, access, groups, tasks, needs, comments
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
    
class FSMEditProjectPhotoItem(StatesGroup):
    item_field = State()

class FSMEditProjectNameItem(StatesGroup):
    item_field = State()

class FSMEditProjectDeskItem(StatesGroup):
    item_field = State()

class FSMEditProjectAccessItem(StatesGroup):
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

def MSG(a_MessageName, a_MessageDesc):
    def UpdateMSG(a_Message : user_messages.Message):
        print(a_Message.m_MessageName, a_Message.m_MessageDesc)
        globals()[a_Message.m_MessageName] = a_Message
    user_messages.MSG(a_MessageName, a_MessageDesc, UpdateMSG, log.GetTimeNow())

# ---------------------------------------------------------
# Сообщения

projects_button_name = "🟥 Проекты"
MSG('base_project_message','''
<b>🟥 Проекты</b>

''')

list_project_button_name = "📃 Список проектов"
MSG('select_project_message','''
Пожалуйста, выберите проект:
''')

MSG('error_find_proj_message','''
❌ Ошибка, проект не найден
''')

MSG('project_open_message',f'''
<b>Проект:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''')

# Создание проекта

add_project_button_name = "✅ Добавить проект"
MSG('project_create_name_message','''
Создание проекта. Шаг №1

Введите название проекта:
''')

MSG('project_create_desc_message','''
Создание проекта. Шаг №2

Введите описание проекта:
''')

MSG('project_create_photo_message','''
Создание проекта. Шаг №3

Загрузите обложку для проекта (Фото):
Она будет отображаться в его описании.
''')

MSG('project_success_create_message','''✅ Проект успешно добавлен!''')

# Редактирование проекта.

edit_project_button_name = "🛠 Редактировать проект"
MSG('project_start_edit_message', '''
Пожалуйста, выберите действие:
''')

MSG('project_select_to_edit_message','''
Выберите проект, который вы хотите отредактировать.
''')

edit_project_photo_button_name = "☐ Изменить изображение в проекте"
MSG('project_edit_photo_message','''
Загрузите новую обложку для проекта (Фото):
Она будет отображаться в его описании.
''')

edit_project_name_button_name = "≂ Изменить название в проекте"
MSG('project_edit_name_message',f'''
Текущее название проекта:
#{name_field}

Введите новое название проекта:
''')

edit_project_desc_button_name = "𝌴 Изменить описание в проекте"
MSG('project_edit_desc_message',f'''
Текущее описание проекта:
#{desc_field}

Введите новое описание проекта:
''')

edit_project_access_button_name = "✋ Изменить доступ к проекту"
MSG('project_edit_access_message',f'''
Текущий доступ к проекту:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''')

MSG('project_success_edit_message','''✅ Проект успешно отредактирован!''')

# Удаление проекта

del_project_button_name = "❌ Удалить проект"
MSG('project_select_to_delete_message','''
Выберите проект, который вы хотите удалить.
Все задачи и потребности в этом проекте так же будут удалены!
''')

MSG('project_success_delete_message','''✅ Проект успешно удалён!''')

# ---------------------------------------------------------
# Работа с кнопками

def GetEditProjectKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_project_photo_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_name_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartProjectKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_project_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_project_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_project_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_project_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start, tasks, needs, comments]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetViewItemInlineKeyboardTemplate(a_ItemID):
    def GetViewItemInlineKeyboard(a_Message, a_UserGroups):
        cur_buttons = [
                keyboard.InlineButtonWithAccess(tasks.list_task_button_name, tasks.select_tasks_prefix, a_ItemID, GetAccess(), user_access.AccessMode.VIEW),
                ]
        return keyboard.MakeInlineKeyboard(cur_buttons, a_UserGroups)
    return GetViewItemInlineKeyboard

# ---------------------------------------------------------
# Обработка сообщений

# стартовое сообщение
async def ProjectsOpen(a_Message : types.message, state = None):
    return simple_message.WorkFuncResult(base_project_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # projectName projectID projectAccess
    return a_Item[1], a_Item[0], a_Item[4]

def ShowMessageTemplate(a_StringMessage, keyboard_template_func = None):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 6):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = str(a_StringMessage).\
                replace(f'#{name_field}', a_Item[1]).\
                replace(f'#{desc_field}', a_Item[2]).\
                replace(f'#{create_datetime_field}', a_Item[5]).\
                replace(f'#{access_field}', a_Item[4])
        keyboard_func = None
        if keyboard_template_func:
            keyboard_func = keyboard_template_func(a_Item[0])
        return simple_message.WorkFuncResult(msg, photo_id = a_Item[3], item_access = a_Item[4], keyboard_func = keyboard_func)
    return ShowMessage

def SimpleMessageTemplateLegacy(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
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
    #TODO: удалить вложенные 
    return simple_message.WorkFuncResult(project_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных проектов

def AddBDItemFunc(a_ItemData, a_UserID):
    res, error = bot_bd.SQLRequestToBD(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], access.GetItemDefaultAccessForModule(module_name) + f";{a_UserID}=+"))

    if error:
        log.Error(f'Пользоватлель {a_UserID}. Ошибка добавления записи в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')
    else:
        log.Success(f'Пользоватлель {a_UserID}. Добавлена запись в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')

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
    return [
            keyboard.ButtonWithAccess(projects_button_name, user_access.AccessMode.VIEW, GetAccess()),
            keyboard.ButtonWithAccess(list_project_button_name, user_access.AccessMode.VIEW, GetAccess()),
            ]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartProjectKeyboardButtons

    # Список проектов
    dp.register_message_handler(simple_message.SimpleMessageTemplateLegacy(ProjectsOpen, defaul_keyboard_func, GetAccess), text = projects_button_name)
    bd_item_view.FirstSelectAndShowBDItemRegisterHandlers(dp, \
            list_project_button_name, \
            table_name, \
            key_name, \
            ShowMessageTemplate(project_open_message, GetViewItemInlineKeyboardTemplate), \
            GetButtonNameAndKeyValueAndAccess, \
            select_project_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Удаление проекта
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            None, \
            bd_item.GetCheckForTextFunc(del_project_button_name), \
            table_name, \
            key_name, \
            None, \
            ProjectPreDelete, \
            ProjectPostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_project_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление проекта
    bd_item_add.AddBDItem3RegisterHandlers(dp, \
            bd_item.GetCheckForTextFunc(add_project_button_name), \
            FSMCreateProject,\
            FSMCreateProject.name,\
            FSMCreateProject.desc, \
            FSMCreateProject.photo,\
            AddBDItemFunc, \
            SimpleMessageTemplateLegacy(project_create_name_message), \
            SimpleMessageTemplateLegacy(project_create_desc_message), \
            SimpleMessageTemplateLegacy(project_create_photo_message), \
            SimpleMessageTemplateLegacy(project_success_create_message), \
            None,\
            None, \
            None, \
            name_field, \
            desc_field, \
            photo_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartProjectKeyboardButtons\
            )

    # Редактирование проекта
    edit_keyboard_func = GetEditProjectKeyboardButtons

    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                None, \
                a_FSM, \
                bd_item.GetCheckForTextFunc(a_ButtonName), \
                project_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(project_success_edit_message), \
                table_name, \
                key_name, \
                None, \
                a_FieldName, \
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                edit_keyboard_func, \
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )

    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(project_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_project_button_name)
    RegisterEdit(edit_project_photo_button_name, FSMEditProjectPhotoItem, project_edit_photo_message, photo_field, bd_item.FieldType.photo)
    RegisterEdit(edit_project_name_button_name, FSMEditProjectNameItem, project_edit_name_message, name_field, bd_item.FieldType.text)
    RegisterEdit(edit_project_desc_button_name, FSMEditProjectDeskItem, project_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_project_access_button_name, FSMEditProjectAccessItem, project_edit_access_message, access_field, bd_item.FieldType.text)
