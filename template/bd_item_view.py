# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access_utils, groups_utils
from template import simple_message, bd_item_delete, bd_item

def ShowBDItemTemplate(a_Bot, a_TableName, a_KeyName, a_WorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    return bd_item_delete.DeleteBDItemTemplate(a_Bot, a_TableName, a_KeyName, a_WorkFunc, None, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = access_mode, delete = False)

def ShowBDItemRegisterHandlers(a_Bot, a_PrevPrefix, a_TableName : str, a_KeyName, a_ShowItemWorkFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    a_Bot.RegisterCallbackHandler(ShowBDItemTemplate(a_Bot, a_TableName, a_KeyName, a_ShowItemWorkFunc, a_PrevPrefix, a_AccessFunc, a_ButtonFunc, access_mode = access_mode), bd_item.GetCheckForPrefixFunc(a_PrevPrefix))
