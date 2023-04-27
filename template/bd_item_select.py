# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message, bd_item

from aiogram import types

def GetBDItemsListKeyboardButtonsTemplate(a_TableName : str, a_PrevPrefix, a_NextPrefix : str, a_GetButtonNameAndKeyValueAndAccessFunc, access_mode = user_access.AccessMode.VIEW):
    def GetBDItemsListKeyboardButtons(a_Message, a_UserGroups):
        #if a_PrevPrefix:
            

        items = bd_item.GetAllItemsTemplate(a_TableName)()
        items_button_list = []
        for t in items:
            bname, key_value, access = a_GetButtonNameAndKeyValueAndAccessFunc(t)
            if access is None:
                access = ''
            if not bname is None and user_access.CheckAccessString(access, a_UserGroups, access_mode):
                items_button_list += [keyboard.Button(bname, key_value)]
        return keyboard.MakeInlineKeyboard(items_button_list, a_NextPrefix)
    return GetBDItemsListKeyboardButtons

def SelectDBItemTemplate(a_TableName : str, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_PrevPrefix, a_NextPrefix, access_mode = user_access.AccessMode.VIEW):
    keyborad_func = GetBDItemsListKeyboardButtonsTemplate(a_TableName, a_PrevPrefix, a_NextPrefix, a_GetButtonNameAndKeyValueAndAccessFunc)
    return simple_message.InfoMessageTemplate(a_StartMessage, keyborad_func, a_AccessFunc, access_mode)

