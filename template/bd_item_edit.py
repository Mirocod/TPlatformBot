# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Редактирование элемента в БД

from bot_sys import user_access, bot_bd
from bot_modules import access_utils, groups_utils
from template import simple_message, bd_item_select, bd_item, bd_item_add

cancel_message = '''
🚫 Редактирование отменено
'''

error_photo_type_message = '''
🚫 Фотографий не найдено
'''

def StartEditBDItemTemplate(a_Bot, a_FSM, a_MessageFunc, a_TableName, a_KeyName, a_Prefix, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = user_access.AccessMode.EDIT):
    return bd_item_add.StartAddBDItemTemplate(a_Bot, a_FSM, a_FSM.item_field, a_MessageFunc, a_TableName, a_KeyName, a_Prefix, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = access_mode)

def FinishEditBDItemTemplate(a_Bot, a_FSM, a_TableName, a_KeyName, a_FieldName, a_MessageFunc, a_PostProcessFunc, a_AccessFunc, a_ButtonFunc, a_OnChangeFunc, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.text):
    def EditBDItemFunc(a_ItemData, a_UserID):
        item_id = a_ItemData[a_KeyName]
        field_value = a_ItemData[a_FieldName]
        res, error = bd_item.EditBDItemInTableTemplate(a_Bot, a_TableName, a_KeyName, a_FieldName)(item_id, field_value)
        if error:
            a_Bot.GetLog().Error(f'Пользователю {a_UserID} не удалось изменить поле в таблице {a_TableName} ключу {a_KeyName}={item_id}. Новое значение поля {a_FieldName}={field_value}. Ошибка: {error}')
        else:
            a_Bot.GetLog().Success(f'Пользователь {a_UserID} изменил поле в таблице {a_TableName} ключу {a_KeyName}={item_id}. Новое значение поля {a_FieldName}={field_value}.')

        a_OnChangeFunc()
        return res, error
    
    return bd_item_add.FinishAddBDItemTemplate(a_Bot, a_FSM, EditBDItemFunc, a_TableName, a_KeyName, a_FieldName, a_MessageFunc, a_PostProcessFunc, a_AccessFunc, a_ButtonFunc, access_mode = access_mode, field_type = field_type)

def EditBDItemRegisterHandlers(a_Bot, a_SelectSource, a_FSM, a_StartMessage, a_EditMessageFunc, a_FinishMessageFunc, a_TableName, a_KeyName, a_FieldName, a_PostProcessFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_AccessFunc, a_AdditionalButtonFunc, a_FinishButtonFunc, a_OnChangeFunc, access_mode = user_access.AccessMode.EDIT, field_type = bd_item.FieldType.text):
    keyboard = bd_item.MixKeyboardFuncTemplate(a_AdditionalButtonFunc, bd_item.GetCancelKeyboardButtonsTemplate(a_Bot, a_AccessFunc, access_mode))

    a_Prefix = bd_item_select.SelectRegisterHandlers(a_Bot, a_SelectSource, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, access_mode = access_mode)

    a_Bot.RegisterCallbackHandler(StartEditBDItemTemplate(a_Bot, a_FSM, a_EditMessageFunc, a_TableName, a_KeyName, a_Prefix, a_AccessFunc, keyboard, a_FinishButtonFunc, access_mode), bd_item.GetCheckForPrefixFunc(a_Prefix))
    if field_type == bd_item.FieldType.photo:
        a_Bot.RegisterMessageHandler(FinishEditBDItemTemplate(a_Bot, a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_PostProcessFunc, a_AccessFunc, a_FinishButtonFunc, a_OnChangeFunc, access_mode, field_type = field_type), content_types = ['photo', 'text'], state = a_FSM.item_field)
    else:
        a_Bot.RegisterMessageHandler(FinishEditBDItemTemplate(a_Bot, a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_PostProcessFunc, a_AccessFunc, a_FinishButtonFunc, a_OnChangeFunc, access_mode, field_type = field_type), state = a_FSM.item_field)
