# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Комментарии

from bot_sys import bot_bd, log, keyboard, user_access
from bot_modules import start, access, groups, projects, tasks, needs
from template import bd_item_view, simple_message, bd_item_delete, bd_item_edit, bd_item, bd_item_add, bd_item_select

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
import sqlite3

class FSMCreateComment(StatesGroup):
    bd_item = State()

class FSMEditDescItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditAccessItem(StatesGroup):
    item_id = State()
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'comments'

table_name = module_name
key_name = 'commentID'
desc_field = 'commentDesc'
access_field = 'commentAccess'
create_datetime_field = 'commentCreateDateTime'
parent_id_field = 'needID'

init_bd_cmds = [f'''CREATE TABLE IF NOT EXISTS {table_name}(
    {key_name} INTEGER PRIMARY KEY,
    {desc_field} TEXT,
    {access_field} TEXT,
    {create_datetime_field} TEXT,
    {parent_id_field} INTEGER
    )''',
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_new}=va', '{user_access.user_access_group_new}=va');"
]

select_comments_prefix = ''

# ---------------------------------------------------------
# Сообщения

comments_button_name = "⚏ Комментарии"
base_comment_message = f'''
<b>{comments_button_name}</b>

'''

list_comment_button_name = "📃 Список комментариев"
select_comment_message = '''
Пожалуйста, выберите комментарий:
'''

error_find_proj_message = '''
❌ Ошибка, комментарий не найден
'''

comment_open_message = f'''
<b>Комментарий</b>

#{desc_field}

Время создания: #{create_datetime_field}
'''

# Создание комментариев

add_comment_button_name = "☑ Добавить комментарий"
comment_create_desc_message = '''
Введите свой комментарий:
'''

comment_success_create_message = '''✅ Комментарий успешно добавлен!'''

# Редактирование комментариев.

edit_comment_button_name = "🛠 Редактировать комментарий"
comment_start_edit_message= '''
Пожалуйста, выберите действие:
'''

comment_select_to_edit_message = '''
Выберите комментарий, который вы хотите отредактировать.
'''

edit_comment_desc_button_name = "𝌴 Изменить комментарий"
comment_edit_desc_message = f'''
Текущий комментарий:
#{desc_field}

Введите отредактированный комментарий:
'''

edit_comment_access_button_name = "✋ Изменить доступ к комментарию"
comment_edit_access_message = f'''
Текущий доступ к комментарию:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

comment_success_edit_message = '''✅ Комментарий успешно отредактирован!'''

# Удаление комментариев

del_comment_button_name = "❌ Удалить комментарий"
comment_select_to_delete_message = '''
Выберите комментарий, которую вы хотите удалить.
'''

comment_success_delete_message = '''✅ Комментарий успешно удалён!'''

# ---------------------------------------------------------
# Работа с кнопками

def GetEditCommentKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = GetModuleButtons() + [
        keyboard.ButtonWithAccess(edit_comment_desc_button_name, user_access.AccessMode.EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_comment_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

def GetStartCommentKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(list_comment_button_name, user_access.AccessMode.VIEW, GetAccess()),
        keyboard.ButtonWithAccess(add_comment_button_name, user_access.AccessMode.ADD, GetAccess()),
        keyboard.ButtonWithAccess(del_comment_button_name, user_access.AccessMode.DELETE, GetAccess()),
        keyboard.ButtonWithAccess(edit_comment_button_name, user_access.AccessMode.EDIT, GetAccess())
        ]
    mods = [start, projects, tasks, needs]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# стартовое сообщение
async def CommentsOpen(a_Message : types.message, state = None):
    return simple_message.WorkFuncResult(base_comment_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # commentDesc commentID commentAccess
    return a_Item[1], a_Item[0], a_Item[2]

def ShowMessageTemplate(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 4):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = a_StringMessage.\
                replace(f'#{desc_field}', a_Item[1]).\
                replace(f'#{create_datetime_field}', a_Item[3]).\
                replace(f'#{access_field}', a_Item[2])
        return simple_message.WorkFuncResult(msg, item_access = a_Item[2])
    return ShowMessage

def SimpleMessageTemplate(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        return simple_message.WorkFuncResult(a_StringMessage)
    return ShowMessage

# Удаление комментариев 

async def CommentPreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 4):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[2]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def CommentPostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Комментарий №{a_ItemID} был удалён пользователем {a_CallbackQuery.from_user.id}.')
    #TODO: удалить вложенные 
    return simple_message.WorkFuncResult(comment_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных комментариев

def AddBDItemFunc(a_ItemData, a_UserID):
    print(a_ItemData)
    res, error = bot_bd.SQLRequestToBD(f'INSERT INTO {table_name}({desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_ItemData[desc_field], access.GetItemDefaultAccessForModule(module_name) + f";{a_UserID}=+", a_ItemData[parent_id_field]))

    if error:
        log.Error(f'Пользоватлель {a_UserID}. Ошибка добавления записи в таблицу {table_name} ({a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')
    else:
        log.Success(f'Пользоватлель {a_UserID}. Добавлена запись в таблицу {table_name} ({a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')

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
    return [keyboard.ButtonWithAccess(comments_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartCommentKeyboardButtons
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
        a_Prefix =  bd_item_select.NextSelectBDItemRegisterHandlers(dp, \
                a_Prefix, \
                needs.parent_id_field, \
                needs.table_name, \
                needs.key_name, \
                needs.GetButtonNameAndKeyValueAndAccess, \
                needs.select_need_message, \
                needs.GetAccess, \
                access_mode = access_mode\
                )
        return a_Prefix


    # Стартовое сообщение
    dp.register_message_handler(simple_message.SimpleMessageTemplate(CommentsOpen, defaul_keyboard_func, GetAccess), text = comments_button_name)

    # Список комментариев
    a_Prefix = RegisterSelectParent(list_comment_button_name, user_access.AccessMode.VIEW)
    bd_item_view.LastSelectAndShowBDItemRegisterHandlers(dp, \
            a_Prefix, parent_id_field, \
            table_name, key_name, \
            ShowMessageTemplate(comment_open_message), \
            GetButtonNameAndKeyValueAndAccess, \
            select_comment_message, \
            GetAccess, \
            defaul_keyboard_func, \
            access_mode = user_access.AccessMode.VIEW\
            )
    global select_comments_prefix
    select_comments_prefix = a_Prefix

    # Удаление комментариев
    a_Prefix = RegisterSelectParent(del_comment_button_name, user_access.AccessMode.DELETE)
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            a_Prefix, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            table_name, \
            key_name, \
            parent_id_field, \
            CommentPreDelete, \
            CommentPostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_comment_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление комментариев
    a_Prefix = RegisterSelectParent(add_comment_button_name, user_access.AccessMode.ADD)
    bd_item_add.AddBDItem1RegisterHandlers(dp, \
            bd_item.GetCheckForPrefixFunc(a_Prefix), \
            FSMCreateComment, \
            AddBDItemFunc, \
            SimpleMessageTemplate(comment_create_desc_message), \
            SimpleMessageTemplate(comment_success_create_message), \
            a_Prefix,\
            needs.table_name, \
            needs.key_name, \
            desc_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartCommentKeyboardButtons,\
            bd_item.FieldType.text
            )

    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        a_Prefix = RegisterSelectParent(a_ButtonName, a_AccessMode)
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                a_Prefix, \
                a_FSM, \
                bd_item.GetCheckForPrefixFunc(a_Prefix), \
                comment_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(comment_success_edit_message), \
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

    # Редактирование комментариев
    edit_keyboard_func = GetEditCommentKeyboardButtons
    dp.register_message_handler(simple_message.InfoMessageTemplate(comment_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_comment_button_name)

    RegisterEdit(edit_comment_desc_button_name, FSMEditDescItem, comment_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_comment_access_button_name, FSMEditAccessItem, comment_edit_access_message, access_field, bd_item.FieldType.text)
