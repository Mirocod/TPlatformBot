# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Языки

from bot_sys import bot_bd, log, keyboard, user_access
from bot_modules import start, access, groups, messages
from template import bd_item_view, simple_message, bd_item_delete, bd_item_edit, bd_item, bd_item_add

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

class FSMCreateLanguage(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditLanguagePhotoItem(StatesGroup):
    item_field = State()

class FSMEditLanguageNameItem(StatesGroup):
    item_field = State()

class FSMEditLanguageDeskItem(StatesGroup):
    item_field = State()

class FSMEditLanguageAccessItem(StatesGroup):
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'languages'

table_name = module_name
key_name = 'languageID'
name_field = 'languageName'
desc_field = 'languageDesc'
photo_field = 'languagePhoto'
access_field = 'languageAccess'
create_datetime_field = 'languageCreateDateTime'

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

languages_button_name = "⚑ Языки"
base_language_message = f'''
<b>{languages_button_name}</b>

'''

list_language_button_name = "📃 Список языков"
select_language_message = '''
Пожалуйста, выберите язык:
'''

error_find_proj_message = '''
❌ Ошибка, язык не найден
'''

language_open_message = f'''
<b>Язык:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
'''

# Создание языка

add_language_button_name = "✅ Добавить язык"
language_create_name_message = '''
Создание языка. Шаг №1

Введите название языка:
'''

language_create_desc_message = '''
Создание языка. Шаг №2

Введите описание языка:
'''

language_create_photo_message = '''
Создание языка. Шаг №3

Загрузите обложку для языка (Фото):
Она будет отображаться в его описании.
'''

language_success_create_message = '''✅ Язык успешно добавлен!'''

# Редактирование языка.

edit_language_button_name = "🛠 Редактировать язык"
language_start_edit_message= '''
Пожалуйста, выберите действие:
'''

language_select_to_edit_message = '''
Выберите язык, который вы хотите отредактировать.
'''

edit_language_photo_button_name = "☐ Изменить изображение в языке"
language_edit_photo_message = '''
Загрузите новую обложку для языка (Фото):
Она будет отображаться в его описании.
'''

edit_language_name_button_name = "≂ Изменить название в языке"
language_edit_name_message = f'''
Текущее название языка:
#{name_field}

Введите новое название языка:
'''

edit_language_desc_button_name = "𝌴 Изменить описание в языке"
language_edit_desc_message = f'''
Текущее описание языка:
#{desc_field}

Введите новое описание языка:
'''

edit_language_access_button_name = "✋ Изменить доступ к языку"
language_edit_access_message = f'''
Текущий доступ к языку:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

language_success_edit_message = '''✅ Язык успешно отредактирован!'''

# Удаление языка

del_language_button_name = "❌ Удалить язык"
language_select_to_delete_message = '''
Выберите язык, которое вы хотите удалить.
'''

language_success_delete_message = '''✅ Язык успешно удален!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditLanguageKeyboardButtons(a_Language, a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_language_photo_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_language_name_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_language_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_language_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartLanguageKeyboardButtons(a_Language, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_language_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_language_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_language_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_language_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start, messages]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetViewItemInlineKeyboardTemplate(a_ItemID):
    def GetViewItemInlineKeyboard(a_Message, a_UserGroups):
        cur_buttons = [
                keyboard.InlineButton(messages.list_message_button_name, messages.select_messages_prefix, a_ItemID, GetAccess(), user_access.AccessMode.VIEW),
                ]
        return keyboard.MakeInlineKeyboard(cur_buttons, a_UserGroups)
    return GetViewItemInlineKeyboard
# ---------------------------------------------------------
# Обработка языков

# стартовое язык
async def LanguagesOpen(a_Language : types.message, state = None):
    return simple_message.WorkFuncResult(base_language_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # languageName languageID languageAccess
    return a_Item[1], a_Item[0], a_Item[4]

def ShowMessageTemplate(a_StringLanguage, keyboard_template_func = None):
    async def ShowLanguage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 6):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = a_StringLanguage.\
                replace(f'#{name_field}', a_Item[1]).\
                replace(f'#{desc_field}', a_Item[2]).\
                replace(f'#{create_datetime_field}', a_Item[5]).\
                replace(f'#{access_field}', a_Item[4])
        keyboard_func = None
        if keyboard_template_func:
            keyboard_func = keyboard_template_func(a_Item[0])
        return simple_message.WorkFuncResult(msg, photo_id = a_Item[3], item_access = a_Item[4], keyboard_func = keyboard_func)
    return ShowLanguage

def SimpleMessageTemplate(a_StringLanguage):
    async def ShowLanguage(a_CallbackQuery : types.CallbackQuery, a_Item):
        return simple_message.WorkFuncResult(a_StringLanguage)
    return ShowLanguage

# Удаление языка 

async def LanguagePreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 6):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[4]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def LanguagePostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Язык №{a_ItemID} был удалён пользователем {a_CallbackQuery.from_user.id}.')
    #TODO: удалить вложенные 
    return simple_message.WorkFuncResult(language_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных языков

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
            keyboard.ButtonWithAccess(languages_button_name, user_access.AccessMode.VIEW, GetAccess()),
            ]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartLanguageKeyboardButtons

    # Список языков
    dp.register_message_handler(simple_message.SimpleMessageTemplate(LanguagesOpen, defaul_keyboard_func, GetAccess), text = languages_button_name)
    bd_item_view.FirstSelectAndShowBDItemRegisterHandlers(dp, \
            list_language_button_name, \
            table_name, \
            key_name, \
            ShowMessageTemplate(language_open_message, GetViewItemInlineKeyboardTemplate), \
            GetButtonNameAndKeyValueAndAccess, \
            select_language_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Удаление языка
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            None, \
            bd_item.GetCheckForTextFunc(del_language_button_name), \
            table_name, \
            key_name, \
            None, \
            LanguagePreDelete, \
            LanguagePostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_language_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление языка
    bd_item_add.AddBDItem3RegisterHandlers(dp, \
            bd_item.GetCheckForTextFunc(add_language_button_name), \
            FSMCreateLanguage,\
            FSMCreateLanguage.name,\
            FSMCreateLanguage.desc, \
            FSMCreateLanguage.photo,\
            AddBDItemFunc, \
            SimpleMessageTemplate(language_create_name_message), \
            SimpleMessageTemplate(language_create_desc_message), \
            SimpleMessageTemplate(language_create_photo_message), \
            SimpleMessageTemplate(language_success_create_message), \
            None,\
            None, \
            None, \
            name_field, \
            desc_field, \
            photo_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartLanguageKeyboardButtons\
            )

    # Редактирование языка
    edit_keyboard_func = GetEditLanguageKeyboardButtons

    def RegisterEdit(a_ButtonName, a_FSM, a_EditLanguage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                None, \
                a_FSM, \
                bd_item.GetCheckForTextFunc(a_ButtonName), \
                language_select_to_edit_message, \
                ShowMessageTemplate(a_EditLanguage), \
                ShowMessageTemplate(language_success_edit_message), \
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

    dp.register_message_handler(simple_message.InfoMessageTemplate(language_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_language_button_name)
    RegisterEdit(edit_language_photo_button_name, FSMEditLanguagePhotoItem, language_edit_photo_message, photo_field, bd_item.FieldType.photo)
    RegisterEdit(edit_language_name_button_name, FSMEditLanguageNameItem, language_edit_name_message, name_field, bd_item.FieldType.text)
    RegisterEdit(edit_language_desc_button_name, FSMEditLanguageDeskItem, language_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_language_access_button_name, FSMEditLanguageAccessItem, language_edit_access_message, access_field, bd_item.FieldType.text)
