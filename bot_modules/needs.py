# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Потребности

from bot_sys import bot_bd, log, keyboard, user_access
from bot_modules import start, access, groups, projects, tasks
from template import bd_item_view, simple_message, bd_item_delete, bd_item_edit, bd_item, bd_item_add, bd_item_select

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

class FSMCreateNeed(StatesGroup):
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
module_name = 'needs'

table_name = module_name
key_name = 'needID'
name_field = 'needName'
desc_field = 'needDesc'
photo_field = 'needPhoto'
access_field = 'needAccess'
create_datetime_field = 'needCreateDateTime'
parent_id_field = 'taskID'

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

needs_button_name = "👉 Потребности"
base_need_message = f'''
<b>{needs_button_name}</b>

'''

list_need_button_name = "📃 Список потребностей"
select_need_message = '''
Пожалуйста, выберите потребность:
'''

error_find_proj_message = '''
❌ Ошибка, потребность не найдена
'''

need_open_message = f'''
<b>Потребность:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
'''

# Создание потребностей

add_need_button_name = "☑ Добавить потребность"
need_create_name_message = '''
Создание потребности. Шаг №1

Введите название потребности:
'''

need_create_desc_message = '''
Создание потребности. Шаг №2

Введите описание потребности:
'''

need_create_photo_message = '''
Создание потребности. Шаг №3

Загрузите обложку для потребности (Фото):
Она будет отображаться в её описании.
'''

need_success_create_message = '''✅ Потребность успешно добавлена!'''

# Редактирование потребностей.

edit_need_button_name = "🛠 Редактировать потребность"
need_start_edit_message= '''
Пожалуйста, выберите действие:
'''

need_select_to_edit_message = '''
Выберите потребность, которую вы хотите отредактировать.
'''

edit_need_photo_button_name = "☐ Изменить изображение у потребности"
need_edit_photo_message = '''
Загрузите новую обложку для потребности (Фото):
Она будет отображаться в её описании.
'''

edit_need_name_button_name = "≂ Изменить название у потребности"
need_edit_name_message = f'''
Текущее название потребности:
#{name_field}

Введите новое название потребности:
'''

edit_need_desc_button_name = "𝌴 Изменить описание у потребности"
need_edit_desc_message = f'''
Текущее описание потребности:
#{desc_field}

Введите новое описание потребности:
'''

edit_need_access_button_name = "✋ Изменить доступ к потребности"
need_edit_access_message = f'''
Текущий доступ к потребности:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

need_success_edit_message = '''✅ Потребность успешно отредактирована!'''

# Удаление потребностей

del_need_button_name = "❌ Удалить потребность"
need_select_to_delete_message = '''
Выберите потребность, которую вы хотите удалить.
Все сообщения в этой потребности так же будут удалены!
'''

need_success_delete_message = '''✅ Потребность успешно удалена!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditNeedKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_need_photo_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_need_name_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_need_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_need_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartNeedKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_need_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_need_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_need_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_need_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# стартовое сообщение
async def NeedsOpen(a_Message : types.message, state = None):
    return simple_message.WorkFuncResult(base_need_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # needName needID needAccess
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

# Удаление потребностей 

async def NeedPreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 6):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[4]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def NeedPostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Потребность №{a_ItemID} была удалена пользователем {a_CallbackQuery.from_user.id}.')
    #TODO: удалить вложенные 
    return simple_message.WorkFuncResult(need_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных потребностей

def AddBDItemFunc(a_ItemData, a_UserID):
    print(a_ItemData)
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
    return [keyboard.ButtonWithAccess(needs_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartNeedKeyboardButtons
    def RegisterSelectParent(a_ButtonName, access_mode):
        a_PrefixBase = a_ButtonName
        a_Prefix =  bd_item_select.FirstSelectBDItemRegisterHandlers(dp, \
                a_PrefixBase, \
                a_ButtonName, \
                projects.table_name, \
                projects.key_name, \
                projects.GetButtonNameAndKeyValueAndAccess, \
                projects.select_project_message, \
                projects.GetAccess, \
                access_mode = access_mode\
                )
        a_Prefix =  bd_item_select.NextSelectBDItemRegisterHandlers(dp, \
                a_Prefix, \
                tasks.parent_id_field, \
                tasks.table_name, \
                tasks.key_name, \
                tasks.GetButtonNameAndKeyValueAndAccess, \
                tasks.select_task_message, \
                tasks.GetAccess, \
                access_mode = access_mode\
                )
        return a_Prefix


    # Стартовое сообщение
    dp.register_message_handler(simple_message.SimpleMessageTemplate(NeedsOpen, defaul_keyboard_func, GetAccess), text = needs_button_name)

    # Список потребностей
    a_Prefix = RegisterSelectParent(list_need_button_name, user_access.AccessMode.VIEW)
    bd_item_view.LastSelectAndShowBDItemRegisterHandlers(dp, \
            a_Prefix, parent_id_field, \
            table_name, key_name, \
            ShowMessageTemplate(need_open_message), \
            GetButtonNameAndKeyValueAndAccess, \
            select_need_message, \
            GetAccess, \
            defaul_keyboard_func, \
            access_mode = user_access.AccessMode.VIEW\
            )

    # Удаление потребностей
    a_Prefix = RegisterSelectParent(del_need_button_name, user_access.AccessMode.DELETE)
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            a_Prefix, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            table_name, \
            key_name, \
            parent_id_field, \
            NeedPreDelete, \
            NeedPostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_need_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление потребностей
    a_Prefix = RegisterSelectParent(add_need_button_name, user_access.AccessMode.ADD)
    bd_item_add.AddBDItem3RegisterHandlers(dp, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            FSMCreateNeed, \
            FSMCreateNeed.name,\
            FSMCreateNeed.desc, \
            FSMCreateNeed.photo,\
            AddBDItemFunc, \
            SimpleMessageTemplate(need_create_name_message), \
            SimpleMessageTemplate(need_create_desc_message), \
            SimpleMessageTemplate(need_create_photo_message), \
            SimpleMessageTemplate(need_success_create_message), \
            a_Prefix,\
            tasks.table_name, \
            tasks.key_name, \
            name_field, \
            desc_field, \
            photo_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartNeedKeyboardButtons\
            )

    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        a_Prefix = RegisterSelectParent(a_ButtonName, a_AccessMode)
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                a_Prefix, \
                a_FSM, \
                bd_item.GetCheckForPrefixFunc(a_Prefix), \
                need_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(need_success_edit_message), \
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

    # Редактирование потребностей
    edit_keyboard_func = GetEditNeedKeyboardButtons
    dp.register_message_handler(simple_message.InfoMessageTemplate(need_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_need_button_name)

    RegisterEdit(edit_need_photo_button_name, FSMEditPhotoItem, need_edit_photo_message, photo_field, bd_item.FieldType.photo)
    RegisterEdit(edit_need_name_button_name, FSMEditNameItem, need_edit_name_message, name_field, bd_item.FieldType.text)
    RegisterEdit(edit_need_desc_button_name, FSMEditDeskItem, need_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_need_access_button_name, FSMEditAccessItem, need_edit_access_message, access_field, bd_item.FieldType.text)
