# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message, bd_item_select, bd_item_delete

from aiogram import types

'''
class TableListParam():
    def __init__(self, a_TableName : str, a_KeyName : str, a_GetButtonNameAndKeyValueAndAccessFunc):
        self.table_name = a_TableName
        self.key_name = a_KeyName
        self.get_bname_and_key_value_func = a_GetButtonNameAndKeyValueAndAccessFunc
'''

def ShowBDItemTemplate(a_TableName, a_KeyName, a_WorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    return bd_item_delete.DeleteBDItemTemplate(a_TableName, a_KeyName, a_WorkFunc, None, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = access_mode, delete = False)

def SelectAndShowBDItemRegisterHandlers(dp, a_RequestButtonName, a_TableName : str, a_KeyName, a_ShowItemWorkFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    a_Prefix = f'select_{a_TableName}_{a_KeyName}:'
    sel_handler = bd_item_select.SelectDBItemTemplate(a_TableName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode)
    dp.register_message_handler(sel_handler, text = a_RequestButtonName)
    dp.register_callback_query_handler(ShowBDItemTemplate(a_TableName, a_KeyName, a_ShowItemWorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode), lambda x: x.data.startswith(a_Prefix))

    return sel_handler
