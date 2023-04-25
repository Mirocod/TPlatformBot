# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Простые информационные сообщения

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message

from aiogram import types

def GetAllItemsTemplate(a_TableName):
    def GetAllItems():
        return bot_bd.SelectBDTemplate(a_TableName)()
    return GetAllItems

def GetBDItemTemplate(a_TableName : str, a_KeyName : str):
    def GetBDItem(a_KeyValue):
        return bot_bd.SQLRequestToBD(f'SELECT * FROM {a_TableName} WHERE {a_KeyName} = ?', param = ([a_KeyValue]))
    return GetBDItem

def GetBDItemsListKeyboardButtonsTemplate(a_TableName : str, a_Prefix : str, a_GetButtonNameAndKeyValueAndAccessFunc, access_mode = user_access.AccessMode.VIEW):
    def GetBDItemsListKeyboardButtons(a_UserGroups):
        items = GetAllItemsTemplate(a_TableName)()
        items_button_list = []
        for t in items:
            bname, key_value, access = a_GetButtonNameAndKeyValueAndAccessFunc(t)
            if not bname is None and user_access.CheckAccessString(access, a_UserGroups, access_mode):
                items_button_list += [keyboard.Button(bname, key_value)]
        return keyboard.MakeInlineKeyboard(items_button_list, a_Prefix)
    return GetBDItemsListKeyboardButtons
'''
class TableListParam():
    def __init__(self, a_TableName : str, a_KeyName : str, a_GetButtonNameAndKeyValueAndAccessFunc):
        self.table_name = a_TableName
        self.key_name = a_KeyName
        self.get_bname_and_key_value_func = a_GetButtonNameAndKeyValueAndAccessFunc
'''
def SelectDBItemTemplate(a_TableName : str, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode = user_access.AccessMode.VIEW):
    keyborad_func = GetBDItemsListKeyboardButtonsTemplate(a_TableName, a_Prefix, a_GetButtonNameAndKeyValueAndAccessFunc)
    return simple_message.InfoMessageTemplate(a_StartMessage, keyborad_func, a_AccessFunc, access_mode)

def ShowBDItemTemplate(a_TableName, a_KeyName, a_WorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    async def ShowBDItem(a_CallbackQuery : types.CallbackQuery):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        item_id = str(a_CallbackQuery.data).replace(a_Prefix, '')
        item = GetBDItemTemplate(a_TableName, a_KeyName)(item_id)
        if len(item) < 1:
            msg = f'Элемент {item_id} не найден в таблице {a_TableName}'
            log.Error(msg)
            await bot.send_message(a_CallbackQuery.from_user.id, msg, reply_markup = a_ButtonFunc(user_groups))
            return None, None

        return await a_WorkFunc(a_CallbackQuery, item[0])
    return simple_message.SimpleMessageTemplate(ShowBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def SelectAndShowBDItemRegisterHandlers(dp, a_RequestButtonName, a_TableName : str, a_KeyName, a_ShowItemWorkFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.VIEW):
    a_Prefix = f'select_{a_TableName}_{a_KeyName}:'
    sel_handler = SelectDBItemTemplate(a_TableName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode)
    dp.register_message_handler(sel_handler, text = a_RequestButtonName)
    dp.register_callback_query_handler(ShowBDItemTemplate(a_TableName, a_KeyName, a_ShowItemWorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode), lambda x: x.data.startswith(a_Prefix))

    return sel_handler
