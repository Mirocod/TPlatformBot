# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# удаление элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access, groups
from template import simple_message, bd_item_select, bd_item

from aiogram import types

def DeleteBDItemTemplate(a_TableName, a_KeyName, a_PreDeleteWorkFunc, a_PostDeleteWorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, delete = True, access_mode = user_access.AccessMode.DELETE):
    async def DeleteBDItem(a_CallbackQuery : types.CallbackQuery, state = None):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        item_id = str(a_CallbackQuery.data).replace(a_Prefix, '')
        check, res_of_pre_del = await bd_item.CheckAccessBDItemTemplate(a_TableName, a_KeyName, item_id, a_PreDeleteWorkFunc, access_mode)(a_CallbackQuery)

        if not check is None:
            return check
        if not delete:
            return res_of_pre_del

        result, error = bd_item.DeleteBDItemInTableTemplate(a_TableName, a_KeyName)(item_id)
        if not error is None:
            msg = error
            log.Error(error)
            return simple_message.WorkFuncResult(error)

        return await a_PostDeleteWorkFunc(a_CallbackQuery, item_id)

    return simple_message.SimpleMessageTemplateLegacy(DeleteBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def DeleteBDItemRegisterHandlers(dp, a_PrevPrefix, a_StartCheckFunc, a_TableName : str, a_KeyName, a_ParentIDFieldName,a_PreDeleteWorkFunc, a_PostDeleteWorkFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.DELETE):
    reg_func = dp.register_message_handler
    if a_ParentIDFieldName:
        reg_func = dp.register_callback_query_handler
    
    a_Prefix = bd_item.HashPrefix(f'delete_{a_TableName}_{a_KeyName}:')
    sel_handler = bd_item_select.SelectDBItemTemplate(a_TableName, a_ParentIDFieldName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_PrevPrefix, a_Prefix, access_mode)
    reg_func(sel_handler, a_StartCheckFunc)
    dp.register_callback_query_handler(DeleteBDItemTemplate(a_TableName, a_KeyName, a_PreDeleteWorkFunc, a_PostDeleteWorkFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode), bd_item.GetCheckForPrefixFunc(a_Prefix))

