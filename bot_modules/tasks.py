# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Задачи

from bot_sys import bot_bd, log, keyboard, user_access
from bot_modules import start, access, groups, projects, needs
from template import bd_item_view, simple_message, bd_item_delete, bd_item_edit, bd_item, bd_item_add, bd_item_select

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

class FSMCreateTask(StatesGroup):
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
module_name = 'tasks'

table_name = module_name
key_name = 'taskID'
name_field = 'taskName'
desc_field = 'taskDesc'
photo_field = 'taskPhoto'
access_field = 'taskAccess'
create_datetime_field = 'taskCreateDateTime'
parent_id_field = 'projectID'

init_bd_cmds = [f'''CREATE TABLE IF NOT EXISTS {table_name}(
    {key_name} INTEGER PRIMARY KEY,
    {name_field} TEXT,
    {desc_field} TEXT,
    {photo_field} TEXT,
    {access_field} TEXT,
    {create_datetime_field} TEXT,
    {parent_id_field} INTEGER
    )''',
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_new}=va', '{user_access.user_access_group_new}=va');"
]

# ---------------------------------------------------------
# Сообщения

tasks_button_name = "✎ Задачи"
base_task_message = '''
<b>✎ Задачи</b>

'''

list_task_button_name = "📃 Список задач"
select_task_message = '''
Пожалуйста, выберите задачу:
'''

error_find_proj_message = '''
❌ Ошибка, задача не найдена
'''

task_open_message = f'''
<b>Задача:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
'''

# Создание задачи

add_task_button_name = "☑ Добавить задачу"
task_create_name_message = '''
Создание задачи. Шаг №1

Введите название задачи:
'''

task_create_desc_message = '''
Создание задачи. Шаг №2

Введите описание задачи:
'''

task_create_photo_message = '''
Создание задачи. Шаг №3

Загрузите обложку для задачи (Фото):
Она будет отображаться в её описании.
'''

task_success_create_message = '''✅ Задача успешно добавлена!'''

# Редактирование задачи.

edit_task_button_name = "🛠 Редактировать задачу"
task_start_edit_message= '''
Пожалуйста, выберите действие:
'''

task_select_to_edit_message = '''
Выберите задачу, которую вы хотите отредактировать.
'''

edit_task_photo_button_name = "☐ Изменить изображение у задачи"
task_edit_photo_message = '''
Загрузите новую обложку для задачи (Фото):
Она будет отображаться в её описании.
'''

edit_task_name_button_name = "≂ Изменить название у задачи"
task_edit_name_message = f'''
Текущее название задачи:
#{name_field}

Введите новое название задачи:
'''

edit_task_desc_button_name = "𝌴 Изменить описание у задачи"
task_edit_desc_message = f'''
Текущее описание задачи:
#{desc_field}

Введите новое описание задачи:
'''

edit_task_access_button_name = "✋ Изменить доступ к задаче"
task_edit_access_message = f'''
Текущий доступ к задаче:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

task_success_edit_message = '''✅ Задача успешно отредактирована!'''

# Удаление задачи

del_task_button_name = "❌ Удалить задачу"
task_select_to_delete_message = '''
Выберите задачу, которую вы хотите удалить.
Все потребности в этой задачае так же будут удалены!
'''

task_success_delete_message = '''✅ Задача успешно удалена!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditTaskKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_task_photo_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_task_name_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_task_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_task_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartTaskKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_task_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_task_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_task_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_task_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start, projects, needs]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# стартовое сообщение
async def TasksOpen(a_Message : types.message, state = None):
    return simple_message.WorkFuncResult(base_task_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # taskName taskID taskAccess
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
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        return simple_message.WorkFuncResult(a_StringMessage)
    return ShowMessage

# Удаление задачи 

async def TaskPreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 6):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[4]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def TaskPostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Задача №{a_ItemID} была удалена пользователем {a_CallbackQuery.from_user.id}.')
    #TODO: удалить вложенные 
    return simple_message.WorkFuncResult(task_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных задач

def AddBDItemFunc(a_ItemData, a_UserID):
    res, error = bot_bd.SQLRequestToBD(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], access.GetItemDefaultAccessForModule(module_name) + f";{a_UserID}=+", a_ItemData[parent_id_field]))

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
    return [keyboard.ButtonWithAccess(tasks_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartTaskKeyboardButtons
    def RegisterSelectParent(a_ButtonName, access_mode):
        a_PrefixBase = a_ButtonName
        return bd_item_select.FirstSelectBDItemRegisterHandlers(dp, \
                a_PrefixBase, \
                a_ButtonName, \
                projects.table_name, \
                projects.key_name, \
                projects.GetButtonNameAndKeyValueAndAccess, \
                projects.select_project_message, \
                projects.GetAccess, access_mode = access_mode\
                )

    # Стартовое сообщение
    dp.register_message_handler(simple_message.SimpleMessageTemplate(TasksOpen, defaul_keyboard_func, GetAccess), text = tasks_button_name)

    # Список задач
    a_Prefix = RegisterSelectParent(list_task_button_name, user_access.AccessMode.VIEW)
    bd_item_view.LastSelectAndShowBDItemRegisterHandlers(dp, \
            a_Prefix, parent_id_field, \
            table_name, key_name, \
            ShowMessageTemplate(task_open_message), \
            GetButtonNameAndKeyValueAndAccess, \
            select_task_message, \
            GetAccess, \
            defaul_keyboard_func, \
            access_mode = user_access.AccessMode.VIEW\
            )

    # Удаление задачи
    a_Prefix = RegisterSelectParent(del_task_button_name, user_access.AccessMode.DELETE)
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            a_Prefix, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            table_name, \
            key_name, \
            parent_id_field, \
            TaskPreDelete, \
            TaskPostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_task_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление задачи
    a_Prefix = RegisterSelectParent(add_task_button_name, user_access.AccessMode.ADD)
    bd_item_add.AddBDItem3RegisterHandlers(dp, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            FSMCreateTask, \
            FSMCreateTask.name,\
            FSMCreateTask.desc, \
            FSMCreateTask.photo,\
            AddBDItemFunc, \
            SimpleMessageTemplate(task_create_name_message), \
            SimpleMessageTemplate(task_create_desc_message), \
            SimpleMessageTemplate(task_create_photo_message), \
            SimpleMessageTemplate(task_success_create_message), \
            a_Prefix,\
            projects.table_name, \
            projects.key_name, \
            name_field, \
            desc_field, \
            photo_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartTaskKeyboardButtons\
            )

    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        a_Prefix = RegisterSelectParent(a_ButtonName, a_AccessMode)
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                a_Prefix, \
                a_FSM, \
                bd_item.GetCheckForPrefixFunc(a_Prefix), \
                task_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(task_success_edit_message), \
                table_name, \
                key_name, \
                parent_id_field, \
                a_FieldName, \
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                edit_keyboard_func, \
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )

    # Редактирование задачи
    edit_keyboard_func = GetEditTaskKeyboardButtons
    dp.register_message_handler(simple_message.InfoMessageTemplate(task_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_task_button_name)

    RegisterEdit(edit_task_photo_button_name, FSMEditPhotoItem, task_edit_photo_message, photo_field, bd_item.FieldType.photo)
    RegisterEdit(edit_task_name_button_name, FSMEditNameItem, task_edit_name_message, name_field, bd_item.FieldType.text)
    RegisterEdit(edit_task_desc_button_name, FSMEditDeskItem, task_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_task_access_button_name, FSMEditAccessItem, task_edit_access_message, access_field, bd_item.FieldType.text)
