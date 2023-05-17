# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Работа с элементом в БД
from enum import Enum

from bot_sys import user_access, bot_bd, keyboard, bot_messages
from bot_modules import groups_utils, access_utils
from template import simple_message

from aiogram import types

import hashlib
def md5(a_Str):
    return hashlib.md5(a_Str.encode('utf-8')).hexdigest()

item_not_found = 'Элемент {item_id} не найден в таблице {a_TableName}'
skip_button_name = "⏩ Пропустить"
canсel_button_name = "🚫 Отменить"

def HashPrefix(a_Str):
    # callback data в сообщении имеет ограниченную длину, поэтому сокращаем префикс
    #a_Bot.GetLog().Info(f'HashPrefix {md5(a_Str)[0:8]}: - {a_Str}')
    return f'{md5(a_Str)[0:8]}:'

class FieldType(Enum):
    text = 'text'
    photo = 'photo'

def GetCheckForPrefixFunc(a_Prefix):
    return lambda x: x.data.startswith(a_Prefix)

def GetCheckForTextFunc(a_Text):
    return lambda x: x.text == str(a_Text)

def GetCheckForCommandsFunc(a_Commands):
    return lambda x: x.commands == a_Commands

def GetKeyDataFromCallbackMessage(a_Message, a_Prefix):
    key_item_id = None
    if a_Prefix and hasattr(a_Message, 'data'):
        key_item_id = str(a_Message.data).replace(a_Prefix, '')
    return key_item_id

def GetCancelKeyboardButtonsTemplate(a_AccessFunc, a_AccessMode):
    def GetCancelKeyboardButtons(a_Message, a_UserGroups):
        cur_buttons = [
            keyboard.ButtonWithAccess(canсel_button_name, a_AccessMode, a_AccessFunc()),
        ]
        return keyboard.MakeButtons(cur_buttons, a_UserGroups)
    return GetCancelKeyboardButtons

def GetSkipAndCancelKeyboardButtonsTemplate(a_AccessFunc, a_AccessMode):
    def GetSkipAndCancelKeyboardButtons(a_Message, a_UserGroups):
        cur_buttons = [
            keyboard.ButtonWithAccess(skip_button_name, a_AccessMode, a_AccessFunc()),
            keyboard.ButtonWithAccess(canсel_button_name, a_AccessMode, a_AccessFunc()),
        ]
        return keyboard.MakeButtons(cur_buttons, a_UserGroups)
    return GetSkipAndCancelKeyboardButtons

def GetAllItemsTemplate(a_Bot, a_TableName):
    def GetAllItems():
        return bot_bd.SelectBDTemplate(a_Bot, a_TableName)()
    return GetAllItems

def GetBDItemsTemplate(a_Bot, a_TableName : str, a_KeyName : str):
    def GetBDItem(a_KeyValue):
        return a_Bot.SQLRequest(f'SELECT * FROM {a_TableName} WHERE {a_KeyName} = ?', param = ([a_KeyValue]))
    return GetBDItem

def DeleteBDItemInTableTemplate(a_Bot, a_TableName : str, a_KeyName : str):
    def DeleteBDItem(a_KeyValue):
        return a_Bot.SQLRequest(f'DELETE FROM {a_TableName} WHERE {a_KeyName} = ?', commit = True, return_error = True, param = ([a_KeyValue]))
    return DeleteBDItem

def EditBDItemInTableTemplate(a_Bot, a_TableName : str, a_KeyName : str, a_FieldName : str):
    def EditBDItemInTable(a_KeyValue, a_FieldValue):
        return a_Bot.SQLRequest(f'UPDATE {a_TableName} SET {a_FieldName}=? WHERE {a_KeyName} = ?', commit = True, return_error = True, param = ([a_FieldValue, a_KeyValue]))
    return EditBDItemInTable

def CheckAccessBDItemTemplate(a_Bot, a_TableName, a_KeyName, a_KeyValue, a_WorkFunc, a_AccessMode : user_access.AccessMode):
    async def CheckAccessBDItem(a_CallbackQuery : types.CallbackQuery):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups_utils.GetUserGroupData(a_Bot, user_id)
        item_id = a_KeyValue
        item = GetBDItemsTemplate(a_Bot, a_TableName, a_KeyName)(item_id)
        if len(item) < 1:
            msg = item_not_found.replace('{item_id}', str(item_id)).replace('{a_TableName}', a_TableName)
            a_Bot.GetLog().Error(msg)
            return simple_message.WorkFuncResult(bot_messages.MakeBotMessage(msg)), None

        result_work_func = await a_WorkFunc(a_CallbackQuery, item[0])
        if result_work_func is None or result_work_func.m_BotMessage is None:
            return result_work_func, result_work_func

        if not result_work_func.item_access is None and not user_access.CheckAccessString(result_work_func.item_access, user_groups, a_AccessMode):
            return simple_message.WorkFuncResult(bot_messages.MakeBotMessage(access_utils.access_denied_message)), None

        return None, result_work_func
    return CheckAccessBDItem
