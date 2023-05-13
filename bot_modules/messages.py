# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Сообщения

from bot_sys import bot_bd, log, keyboard, user_access, user_messages
from bot_modules import start, access, groups, languages
from template import bd_item_view, simple_message, bd_item_delete, bd_item_edit, bd_item, bd_item_add, bd_item_select

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

class FSMCreateMessage(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditMessagePhotoItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditMessageNameItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditMessageDescItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditMessageAccessItem(StatesGroup):
    item_id = State()
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'messages'

table_name = module_name
key_name = 'messageID'
name_field = 'messageName'
desc_field = 'messageDesc'
photo_field = 'messagePhoto'
access_field = 'messageAccess'
create_datetime_field = 'messageCreateDateTime'
parent_id_field = 'languageID'

init_bd_cmds = [f'''CREATE TABLE IF NOT EXISTS {table_name}(
    {key_name} INTEGER PRIMARY KEY,
    {name_field} TEXT,
    {desc_field} TEXT,
    {photo_field} TEXT,
    {access_field} TEXT,
    {create_datetime_field} TEXT,
    {parent_id_field} INTEGER,
    UNIQUE({key_name}),
    UNIQUE({name_field}, {parent_id_field})
    )''',
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_all}=-', '{user_access.user_access_group_all}=-');"
]

select_messages_prefix = ''

# ---------------------------------------------------------
# Сообщения

messages_button_name = "✉ Сообщения"
base_message_message = '''
<b>✎ Сообщения</b>

'''

list_message_button_name = "📃 Список сообщений"
select_message_message = '''
Пожалуйста, выберите сообщение:
'''

error_find_proj_message = '''
❌ Ошибка, сообщенийа не найдена
'''

message_open_message = f'''
<b>Сообщение:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
'''

# Создание сообщения

add_message_button_name = "☑ Добавить сообщение"
message_create_name_message = '''
Создание сообщения. Шаг №1

Введите название сообщения:
'''

message_create_desc_message = '''
Создание сообщения. Шаг №2

Введите описание сообщения:
'''

message_create_photo_message = '''
Создание сообщения. Шаг №3

Загрузите обложку для сообщения (Фото):
Она будет отображаться в её описании.
'''

message_success_create_message = '''✅ Сообщение успешно добавлено!'''

# Редактирование сообщения.

edit_message_button_name = "🛠 Редактировать сообщение"
message_start_edit_message= '''
Пожалуйста, выберите действие:
'''

message_select_to_edit_message = '''
Выберите сообщение, которую вы хотите отредактировать.
'''

edit_message_photo_button_name = "☐ Изменить изображение у сообщения"
message_edit_photo_message = '''
Загрузите новую обложку для сообщения (Фото):
Она будет отображаться в её описании.
'''

edit_message_name_button_name = "≂ Изменить название у сообщения"
message_edit_name_message = f'''
Текущее название сообщения:
#{name_field}

Введите новое название сообщения:
'''

edit_message_desc_button_name = "𝌴 Изменить описание у сообщения"
message_edit_desc_message = f'''
Текущее описание сообщения:
#{desc_field}

Введите новое описание сообщения:
'''

edit_message_access_button_name = "✋ Изменить доступ к сообщению"
message_edit_access_message = f'''
Текущий доступ к сообщению:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

message_success_edit_message = '''✅ Сообщение успешно отредактировано!'''

# Удаление сообщения

del_message_button_name = "❌ Удалить сообщение"
message_select_to_delete_message = '''
Выберите сообщение, которую вы хотите удалить.
'''

message_success_delete_message = '''✅ Сообщение успешно удалено!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditMessageKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_message_photo_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_message_name_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_message_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_message_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartMessageKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_message_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_message_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_message_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_message_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start, languages]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetViewItemInlineKeyboardTemplate(a_ItemID):
    def GetViewItemInlineKeyboard(a_Message, a_UserGroups):
        cur_buttons = [
                #keyboard.InlineButtonWithAccess(needs.list_need_button_name, needs.select_needs_prefix, a_ItemID, GetAccess(), user_access.AccessMode.VIEW),
                ]
        return keyboard.MakeInlineKeyboard(cur_buttons, a_UserGroups)
    return GetViewItemInlineKeyboard

# ---------------------------------------------------------
# Обработка сообщений

# стартовое сообщение
async def MessagesOpen(a_Message : types.message, state = None):
    return simple_message.WorkFuncResult(base_message_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # messageName messageID messageAccess
    return a_Item[1], a_Item[0], a_Item[4]

def ShowMessageTemplate(a_StringMessage, keyboard_template_func = None):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 6):
            return simple_message.WorkFuncResult(error_find_proj_message)

        if message_success_edit_message == a_StringMessage:
            FlushMessages()
            # TODO FlushMessages происходит рано. Нужно после изменений
        msg = a_StringMessage.\
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

# Удаление сообщения 

async def MessagePreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 6):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[4]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def MessagePostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Сообщение №{a_ItemID} была удалена пользователем {a_CallbackQuery.from_user.id}.')
    #TODO: удалить вложенные 
    FlushMessages()
    return simple_message.WorkFuncResult(message_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных сообщений

def AddBDItemFunc(a_ItemData, a_UserID):
    res, error = bot_bd.SQLRequestToBD(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], access.GetItemDefaultAccessForModule(module_name) + f";{a_UserID}=+", a_ItemData[parent_id_field]))

    if error:
        log.Error(f'Пользоватлель {a_UserID}. Ошибка добавления записи в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')
    else:
        log.Success(f'Пользоватлель {a_UserID}. Добавлена запись в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')

    FlushMessages()
    return res, error

# ---------------------------------------------------------
# API

def AddOrIgnoreMessage(a_Message : user_messages.Message):
    return bot_bd.SQLRequestToBD(f'INSERT OR IGNORE INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_Message.m_PhotoID, a_Message.m_MessageName, a_Message.m_MessageDesc, access.GetItemDefaultAccessForModule(module_name), languages.GetLangID(a_Message.m_Language)))

def FlushMessages():
    msg = user_messages.GetMessages()
    for lang, msg_dict in msg.items():
        for msg_name, message in msg_dict.items():
            AddOrIgnoreMessage(message)

    msgs_bd = bd_item.GetAllItemsTemplate(table_name)()
    if msgs_bd:
        for m in msgs_bd:
            name = m[1]
            lang_id = m[6]
            lang_name = languages.GetLangName(lang_id)
            new_msg = user_messages.Message(name, m[2], lang_name, m[3], log.GetTimeNow())
            if not msg.get(lang_name, None):
                msg[lang_name] = {}
            msg[lang_name][name] = new_msg
    user_messages.UpdateSignal(log.GetTimeNow())

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(messages_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartMessageKeyboardButtons
    def RegisterSelectParent(a_ButtonName, access_mode):
        a_PrefixBase = a_ButtonName
        return bd_item_select.FirstSelectBDItemRegisterHandlers(dp, \
                a_PrefixBase, \
                a_ButtonName, \
                languages.table_name, \
                languages.key_name, \
                languages.GetButtonNameAndKeyValueAndAccess, \
                languages.select_language_message, \
                languages.GetAccess, access_mode = access_mode\
                )

    # Стартовое сообщение
    dp.register_message_handler(simple_message.SimpleMessageTemplateLegacy(MessagesOpen, defaul_keyboard_func, GetAccess), text = messages_button_name)

    # Список сообщений
    a_Prefix = RegisterSelectParent(list_message_button_name, user_access.AccessMode.VIEW)
    bd_item_view.LastSelectAndShowBDItemRegisterHandlers(dp, \
            a_Prefix, parent_id_field, \
            table_name, key_name, \
            ShowMessageTemplate(message_open_message), \
            GetButtonNameAndKeyValueAndAccess, \
            select_message_message, \
            GetAccess, \
            defaul_keyboard_func, \
            access_mode = user_access.AccessMode.VIEW\
            )
    global select_messages_prefix
    select_messages_prefix = a_Prefix

    # Удаление сообщения
    a_Prefix = RegisterSelectParent(del_message_button_name, user_access.AccessMode.DELETE)
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            a_Prefix, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            table_name, \
            key_name, \
            parent_id_field, \
            MessagePreDelete, \
            MessagePostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_message_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление сообщения
    a_Prefix = RegisterSelectParent(add_message_button_name, user_access.AccessMode.ADD)
    bd_item_add.AddBDItem3RegisterHandlers(dp, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            FSMCreateMessage, \
            FSMCreateMessage.name,\
            FSMCreateMessage.desc, \
            FSMCreateMessage.photo,\
            AddBDItemFunc, \
            SimpleMessageTemplateLegacy(message_create_name_message), \
            SimpleMessageTemplateLegacy(message_create_desc_message), \
            SimpleMessageTemplateLegacy(message_create_photo_message), \
            SimpleMessageTemplateLegacy(message_success_create_message), \
            a_Prefix,\
            languages.table_name, \
            languages.key_name, \
            name_field, \
            desc_field, \
            photo_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartMessageKeyboardButtons\
            )

    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        a_Prefix = RegisterSelectParent(a_ButtonName, a_AccessMode)
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                a_Prefix, \
                a_FSM, \
                bd_item.GetCheckForPrefixFunc(a_Prefix), \
                message_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(message_success_edit_message), \
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

    # Редактирование сообщения
    edit_keyboard_func = GetEditMessageKeyboardButtons
    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(message_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_message_button_name)

    RegisterEdit(edit_message_photo_button_name, FSMEditMessagePhotoItem, message_edit_photo_message, photo_field, bd_item.FieldType.photo)
    RegisterEdit(edit_message_name_button_name, FSMEditMessageNameItem, message_edit_name_message, name_field, bd_item.FieldType.text)
    RegisterEdit(edit_message_desc_button_name, FSMEditMessageDescItem, message_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_message_access_button_name, FSMEditMessageAccessItem, message_edit_access_message, access_field, bd_item.FieldType.text)
