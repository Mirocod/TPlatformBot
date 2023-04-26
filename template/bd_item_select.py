# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message

from aiogram import types

def GetAllItemsTemplate(a_TableName):
    def GetAllItems():
        return bot_bd.SelectBDTemplate(a_TableName)()
    return GetAllItems

def GetBDItemsTemplate(a_TableName : str, a_KeyName : str):
    def GetBDItem(a_KeyValue):
        return bot_bd.SQLRequestToBD(f'SELECT * FROM {a_TableName} WHERE {a_KeyName} = ?', param = ([a_KeyValue]))
    return GetBDItem

def GetBDItemsListKeyboardButtonsTemplate(a_TableName : str, a_Prefix : str, a_GetButtonNameAndKeyValueAndAccessFunc, access_mode = user_access.AccessMode.VIEW):
    def GetBDItemsListKeyboardButtons(a_UserGroups):
        items = GetAllItemsTemplate(a_TableName)()
        items_button_list = []
        for t in items:
            bname, key_value, access = a_GetButtonNameAndKeyValueAndAccessFunc(t)
            if access is None:
                access = ''
            if not bname is None and user_access.CheckAccessString(access, a_UserGroups, access_mode):
                items_button_list += [keyboard.Button(bname, key_value)]
        return keyboard.MakeInlineKeyboard(items_button_list, a_Prefix)
    return GetBDItemsListKeyboardButtons

def SelectDBItemTemplate(a_TableName : str, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode = user_access.AccessMode.VIEW):
    keyborad_func = GetBDItemsListKeyboardButtonsTemplate(a_TableName, a_Prefix, a_GetButtonNameAndKeyValueAndAccessFunc)
    return simple_message.InfoMessageTemplate(a_StartMessage, keyborad_func, a_AccessFunc, access_mode)

