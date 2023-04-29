# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message, bd_item

from aiogram import types

def GetBDItemsListKeyboardButtonsTemplate(a_TableName : str, a_ParentIDFieldName, a_PrevPrefix, a_NextPrefix : str, a_GetButtonNameAndKeyValueAndAccessFunc, access_mode = user_access.AccessMode.VIEW):
    def GetBDItemsListKeyboardButtons(a_Message, a_UserGroups):
        parent_id = bd_item.GetKeyDataFromCallbackMessage(a_Message, a_PrevPrefix)
        items = []
        if a_ParentIDFieldName and parent_id and parent_id != '':
            items = bd_item.GetBDItemsTemplate(a_TableName, a_ParentIDFieldName)(parent_id)
        else:
            items = bd_item.GetAllItemsTemplate(a_TableName)()

        print('GetBDItemsListKeyboardButtons', parent_id, a_PrevPrefix, a_ParentIDFieldName, "\n", items)
        items_button_list = []
        for t in items:
            print('GetBDItemsListKeyboardButtons items', t)
            bname, key_value, access = a_GetButtonNameAndKeyValueAndAccessFunc(t)
            if access is None:
                access = ''
            if not bname is None and user_access.CheckAccessString(access, a_UserGroups, access_mode):
                b = keyboard.Button(bname, key_value)
                print(bname, key_value, b)
                items_button_list += [b]
        print(items_button_list)
        return keyboard.MakeInlineKeyboard(items_button_list, a_NextPrefix)
    return GetBDItemsListKeyboardButtons

def SelectDBItemTemplate(a_TableName : str, a_ParentIDFieldName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_PrevPrefix, a_NextPrefix, access_mode = user_access.AccessMode.VIEW):
    keyboard_func = GetBDItemsListKeyboardButtonsTemplate(a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_NextPrefix, a_GetButtonNameAndKeyValueAndAccessFunc)
    return simple_message.InfoMessageTemplate(a_StartMessage, keyboard_func, a_AccessFunc, access_mode)

def hash_str(a_Str):
    summ = 0
    for i in a_Str:
        summ += ord(i)
    return f'{summ}:'

def FirstSelectBDItemRegisterHandlers(dp, a_PrefixBase, a_ButtonName, a_TableName : str, a_KeyName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):

    a_Prefix = hash_str(f'first_select_{a_TableName}_{a_KeyName}_in_base_{a_PrefixBase}:')

    sel_handler = SelectDBItemTemplate(a_TableName, None, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, None, a_Prefix, access_mode = access_mode)
    dp.register_message_handler(sel_handler, text = a_ButtonName)

    return a_Prefix, sel_handler

def NextSelectBDItemRegisterHandlers(dp, a_PrevPrefix, a_ParentIDFieldName, a_TableName : str, a_KeyName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    a_Prefix = f'next_select_{a_TableName}_{a_KeyName}_{a_ParentIDFieldName}_after_prefix_{a_PrevPrefix}:'

    sel_handler = SelectDBItemTemplate(a_TableName, a_ParentIDFieldName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_PrevPrefix, a_Prefix, access_mode = access_mode)
    dp.register_callback_query_handler(sel_handler, bd_item.GetCheckForPrefixFunc(a_PrevPrefix))

    return a_Prefix, sel_handler
