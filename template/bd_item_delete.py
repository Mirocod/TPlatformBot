# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# удаление элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message, bd_item_select

from aiogram import types

item_not_found = 'Элемент {item_id} не найден в таблице {a_TableName}'

'''
class TableListParam():
    def __init__(self, a_TableName : str, a_KeyName : str, a_GetButtonNameAndKeyValueAndAccessFunc):
        self.table_name = a_TableName
        self.key_name = a_KeyName
        self.get_bname_and_key_value_func = a_GetButtonNameAndKeyValueAndAccessFunc
'''

def DeleteBDItemInTableTemplate(a_TableName : str, a_KeyName : str):
    def DeleteBDItem(a_KeyValue):
        return bot_bd.SQLRequestToBD(f'DELETE FROM {a_TableName} WHERE {a_KeyName} = ?', commit = True, return_error = True, param = ([a_KeyValue]))
    return DeleteBDItem

def DeleteBDItemTemplate(a_TableName, a_KeyName, a_PreDeleteWorkFunc, a_PostDeleteWorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, delete = True, access_mode = user_access.AccessMode.DELETE):
    async def DeleteBDItem(a_CallbackQuery : types.CallbackQuery):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        item_id = str(a_CallbackQuery.data).replace(a_Prefix, '')
        item = bd_item_select.GetBDItemsTemplate(a_TableName, a_KeyName)(item_id)
        if len(item) < 1:
            msg = item_not_found.replace('{item_id}', str(item_id)).replace('{a_TableName}', a_TableName)
            log.Error(msg)
            return simple_message.WorkFuncResult(msg)

        res_of_pre_del = await a_PreDeleteWorkFunc(a_CallbackQuery, item[0])
        if not delete:
            return res_of_pre_del

        if res_of_pre_del is None or res_of_pre_del.string_message is None:
            return res_of_pre_del

        if not res_of_pre_del.item_access is None and not user_access.CheckAccessString(res_of_pre_del.item_access, user_groups, access_mode):
            return simple_message.WorkFuncResult(access.access_denied_message)

        result, error = DeleteBDItemInTableTemplate(a_TableName, a_KeyName)(item_id)
        if not error is None:
            msg = error
            log.Error(error)
            return simple_message.WorkFuncResult(error)

        return await a_PostDeleteWorkFunc(a_CallbackQuery, item_id)

    return simple_message.SimpleMessageTemplate(DeleteBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def DeleteBDItemRegisterHandlers(dp, a_RequestButtonName, a_TableName : str, a_KeyName, a_PreDeleteWorkFunc, a_PostDeleteWorkFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.DELETE):
    a_Prefix = f'delete_{a_TableName}_{a_KeyName}:'
    sel_handler = bd_item_select.SelectDBItemTemplate(a_TableName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode)
    dp.register_message_handler(sel_handler, text = a_RequestButtonName)
    dp.register_callback_query_handler(DeleteBDItemTemplate(a_TableName, a_KeyName, a_PreDeleteWorkFunc, a_PostDeleteWorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode), lambda x: x.data.startswith(a_Prefix))

