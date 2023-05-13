# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, groups
from template import simple_message, sql_request, bd_item_edit, bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram import types

class FSMRequestToBDAccess(StatesGroup):
    sqlRequest = State()


class FSMEditAccessItem(StatesGroup):
    item_field = State()


class FSMEditDefaultAccessItem(StatesGroup):
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'access'

table_name = 'module_access'
mod_name_field = 'modName'
moduleaccess_field = 'modAccess'
mod_default_access_field = 'itemDefaultAccess'

#TODO: Автоматическое создание init_bd_cmds, необходимо table_name, mod_name_field ... объединить в объект

init_bd_cmds = [f"""CREATE TABLE IF NOT EXISTS {table_name}(
    {mod_name_field} TEXT,
    {moduleaccess_field} TEXT,
    {mod_default_access_field} TEXT,
    UNIQUE({mod_name_field})
);""",
f"INSERT OR IGNORE INTO {table_name} ({mod_name_field}, {moduleaccess_field}, {mod_default_access_field}) VALUES ('{module_name}', '{user_access.user_access_group_new}=-', '{user_access.user_access_group_new}=-');"
]

# ---------------------------------------------------------
# Сообщения

access_start_message = '''
<b> Права пользователей находятся в стадии разработки</b>

Пока можете воспользоваться хардкорным способом через запросы к БД
'''

request_start_message = '''
**Задайте запрос к БД**

Можете воспользоваться следующими шаблонами:
1. `SELECT * FROM users` - Все пользователи
2. `SELECT * FROM module_access` - Все права к модулям
3. `UPDATE module_access SET modAccess = 'NEWACCESS' WHERE modName = 'MODNAME'` - Задать новые права NEWACCESS для модуля MODNAME
'''

help_message = '''
📄 Существует одна БД для работы с правами для модулей
Имя БД: module_access 
Поля:(modName, modAccess)

modAccess - строка
''' + user_access.user_access_readme

access_denied_message = '''
❌ Доступ запрещён!
''' 

access_button_name = "⛀ Доступ пользователей"
sql_request_button_name = "⛁ Запрос к БД для редактирования доступа"
help_button_name = "📄 Информация по редактированию доступа"

# Редактирование доступа.

moduleaccess_select_to_edit_message = '''
Выберите модуль, который вы хотите отредактировать.
'''

edit_moduleaccess_access_button_name = "◇ Изменить доступ к модулю"
moduleaccess_edit_access_message = f'''
Текущий доступ к модулю #{mod_name_field}:
#{moduleaccess_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

edit_moduleaccess_default_access_button_name = "◈ Изменить доступ по умолчанию к модулю "
moduleaccess_edit_default_access_message = f'''
Текущий доступ по умолчанию к модулю #{mod_name_field}:
#{mod_default_access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

moduleaccess_success_edit_message = '''✅ Проект успешно отредактирован!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditAccessKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(sql_request_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_moduleaccess_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_moduleaccess_default_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(help_button_name, user_access.AccessMode.VIEW, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # ButtonName KeyValue Access
    return a_Item[0], a_Item[0], a_Item[1]

def ShowMessageTemplate(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 3):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = a_StringMessage.\
                replace(f'#{mod_name_field}', a_Item[0]).\
                replace(f'#{moduleaccess_field}', a_Item[1]).\
                replace(f'#{mod_default_access_field}', a_Item[2])
        return simple_message.WorkFuncResult(msg, item_access = a_Item[1])
    return ShowMessage

def SimpleMessageTemplateLegacy(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery):
        return simple_message.WorkFuncResult(a_StringMessage)
    return ShowMessage

# ---------------------------------------------------------
# Работа с базой данных 

def GetModuleAccessList():
    return bot_bd.SelectBDTemplate(table_name)()

# ---------------------------------------------------------
# API

def GetAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[1]
    return ''

def GetItemDefaultAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[2]
    return ''

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(access_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetEditAccessKeyboardButtons
    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(access_start_message, defaul_keyboard_func, GetAccess), text = access_button_name)
    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(help_message, defaul_keyboard_func, GetAccess), text = help_button_name)

    sql_request.RequestToBDRegisterHandlers(dp, sql_request_button_name, request_start_message, FSMRequestToBDAccess, defaul_keyboard_func, user_access.AccessMode.ACCEES_EDIT, GetAccess)

    edit_keyboard_func = defaul_keyboard_func
    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.ACCEES_EDIT):
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                None, \
                a_FSM, \
                bd_item.GetCheckForTextFunc(a_ButtonName), \
                moduleaccess_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(moduleaccess_success_edit_message), \
                table_name, \
                mod_name_field, \
                None, \
                a_FieldName, \
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                edit_keyboard_func, \
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )
    RegisterEdit(edit_moduleaccess_access_button_name, FSMEditAccessItem, moduleaccess_edit_access_message, moduleaccess_field, bd_item.FieldType.text, user_access.AccessMode.ACCEES_EDIT)
    RegisterEdit(edit_moduleaccess_default_access_button_name, FSMEditDefaultAccessItem, moduleaccess_edit_default_access_message, mod_default_access_field, bd_item.FieldType.text, user_access.AccessMode.EDIT)
