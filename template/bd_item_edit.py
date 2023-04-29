# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Редактирование элемента в БД

from bot_sys import user_access, bot_bd, log
from bot_modules import access, groups
from template import simple_message, bd_item_select, bd_item, bd_item_add

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

cancel_message = '''
🚫 Редактирование отменено
'''

error_photo_type_message = '''
🚫 Фотографий не найдено
'''

def StartEditBDItemTemplate(a_FSM, a_MessageFunc, a_TableName, a_KeyName, a_Prefix, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = user_access.AccessMode.EDIT):
    return bd_item_add.StartAddBDItemTemplate(a_FSM, a_FSM.item_id, a_MessageFunc, a_TableName, a_KeyName, a_Prefix, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = access_mode)

def FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.text):
    def EditBDItemFunc(a_ItemData, a_UserID):
        item_id = a_ItemData[bd_item_add.parent_id_field_name]
        field_value = a_ItemData[a_FieldName]
        res, error = bd_item.EditBDItemInTableTemplate(a_TableName, a_KeyName, a_FieldName)(item_id, field_value)
        if error:
            log.Error(f'Пользователю {a_UserID} не удалось изменить поле в таблице {a_TableName} ключу {a_KeyName}={item_id}. Новое значение поля {a_FieldName}={field_value}. Ошибка: {error}')
        else:
            log.Success(f'Пользователь {a_UserID} изменил поле в таблице {a_TableName} ключу {a_KeyName}={item_id}. Новое значение поля {a_FieldName}={field_value}.')
        return res, error
    
    return bd_item_add.FinishAddBDItemTemplate(a_FSM, EditBDItemFunc, a_TableName, a_KeyName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, access_mode = access_mode, field_type = field_type)

def EditBDItemRegisterHandlers(dp, a_FSM, a_ButtonName, a_StartMessage, a_EditMessageFunc, a_FinishMessageFunc, a_TableName : str, a_KeyName, a_FieldName, a_GetButtonNameAndKeyValueAndAccessFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.text):
    keyboard_cancel = bd_item.GetCancelKeyboardButtonsTemplate(a_AccessFunc, access_mode)
    a_Prefix = f'edit_{a_TableName}_{a_KeyName}_{a_FieldName}:'
    sel_handler = bd_item_select.SelectDBItemTemplate(a_TableName, None, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, None, a_Prefix, access_mode)
    dp.register_message_handler(sel_handler, text = a_ButtonName)
    dp.register_callback_query_handler(StartEditBDItemTemplate(a_FSM, a_EditMessageFunc, a_TableName, a_KeyName, a_Prefix, a_AccessFunc, keyboard_cancel, a_ButtonFunc, access_mode), bd_item.GetCheckForPrefixFunc(a_Prefix))
    if field_type == bd_item.FieldType.photo:
        dp.register_message_handler(FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_AccessFunc, a_ButtonFunc, access_mode, field_type = field_type), content_types = ['photo', 'text'], state = a_FSM.item_field)
    else:
        dp.register_message_handler(FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_AccessFunc, a_ButtonFunc, access_mode, field_type = field_type), state = a_FSM.item_field)
