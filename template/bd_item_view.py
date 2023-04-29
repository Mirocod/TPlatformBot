# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message, bd_item_select, bd_item_delete, bd_item

from aiogram import types

def ShowBDItemTemplate(a_TableName, a_KeyName, a_WorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    return bd_item_delete.DeleteBDItemTemplate(a_TableName, a_KeyName, a_WorkFunc, None, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = access_mode, delete = False)

def ShowBDItemRegisterHandlers(dp, a_PrevPrefix, a_TableName : str, a_KeyName, a_ShowItemWorkFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    dp.register_callback_query_handler(ShowBDItemTemplate(a_TableName, a_KeyName, a_ShowItemWorkFunc, a_PrevPrefix, a_AccessFunc, a_ButtonFunc, access_mode = access_mode), bd_item.GetCheckForPrefixFunc(a_PrevPrefix))

def FirstSelectAndShowBDItemRegisterHandlers(dp, a_ButtonName, a_TableName : str, a_KeyName, a_ShowItemWorkFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    a_Prefix = bd_item_select.FirstSelectBDItemRegisterHandlers(dp, '', a_ButtonName, a_TableName, a_KeyName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, access_mode = access_mode)
    ShowBDItemRegisterHandlers(dp, a_Prefix, a_TableName, a_KeyName, a_ShowItemWorkFunc, a_AccessFunc, a_ButtonFunc, access_mode = access_mode)

def LastSelectAndShowBDItemRegisterHandlers(dp, a_PrevPrefix, a_ParentIDFieldName, a_TableName : str, a_KeyName, a_ShowItemWorkFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    a_Prefix = bd_item_select.NextSelectBDItemRegisterHandlers(dp, a_PrevPrefix, a_ParentIDFieldName, a_TableName, a_KeyName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, access_mode = access_mode)
    ShowBDItemRegisterHandlers(dp, a_Prefix, a_TableName, a_KeyName, a_ShowItemWorkFunc, a_AccessFunc, a_ButtonFunc, access_mode = access_mode)
