# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Редактирование элемента в БД

from enum import Enum

from bot_sys import user_access, bot_bd, keyboard, log
from bot_modules import access, groups
from template import simple_message, bd_item_select, bd_item

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

canсel_button_name = "🚫 Отменить"

cancel_message = '''
🚫 Редактирование отменено
'''

error_photo_type_message = '''
🚫 Фотографий не найдено
'''

def GetCancelKeyboardButtonsTemplate(a_AccessFunc, a_AccessMode):
    def GetCancelKeyboardButtons(a_UserGroups):
        cur_buttons = [
            keyboard.ButtonWithAccess(canсel_button_name, a_AccessMode, a_AccessFunc())
        ]
        return keyboard.MakeKeyboard(cur_buttons, a_UserGroups)
    return GetCancelKeyboardButtons

class FieldType(Enum):
    text = 'text'
    photo = 'photo'

def StartEditBDItemTemplate(a_FSM, a_MessageFunc, a_TableName, a_KeyName, a_FieldName, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT):
    async def StartEditBDItem(a_CallbackQuery : types.CallbackQuery, state : FSMContext):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        await a_FSM.item_id.set()
        item_id = str(a_CallbackQuery.data).replace(a_Prefix, '')
        res_of_work_func = None
        async with state.proxy() as item_data:
            item_data['item_id'] = item_id

            check, res_of_work_func = await bd_item.CheckAccessBDItemTemplate(a_TableName, a_KeyName, item_id, a_MessageFunc, access_mode)(a_CallbackQuery)

            if not check is None:
                await state.finish()
                return check
        await a_FSM.next()
        return res_of_work_func
    return simple_message.SimpleMessageTemplate(StartEditBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_MessageFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT, field_type = FieldType.text):
    async def FinishEditBDItem(a_Message : types.CallbackQuery, state : FSMContext):
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        error = None
        res_of_work_func = None
        async with state.proxy() as item_data:
            if a_Message.text == canсel_button_name:
                print('canсel_button_name', canсel_button_name)
                await state.finish()
                return simple_message.WorkFuncResult(cancel_message)

            item_id = item_data['item_id']
            check, res_of_work_func = await bd_item.CheckAccessBDItemTemplate(a_TableName, a_KeyName, item_id, a_MessageFunc, access_mode)(a_Message)

            if not check is None:
                await state.finish()
                return check

            field_value = ''
            if field_type == FieldType.photo:
                if a_Message.photo == None or len(a_Message.photo) == 0:
                    await state.finish()
                    return simple_message.WorkFuncResult(error_photo_type_message)
                field_value = a_Message.photo[0].file_id
            else:
                field_value = a_Message.text
            res, error = bd_item.EditBDItemInTableTemplate(a_TableName, a_KeyName, a_FieldName)(item_id, field_value)
            log.Success(f'Изменено поле в таблице {a_TableName} ключу {a_KeyName}={item_id}. Новое значение поля {a_FieldName}={field_value}. Пользователь {user_id}.')
        await state.finish()
        if error:
            return simple_message.WorkFuncResult(error)
        return res_of_work_func

    return simple_message.SimpleMessageTemplate(FinishEditBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def EditBDItemRegisterHandlers(dp, a_FSM, a_ButtonName, a_StartMessage, a_EditMessageFunc, a_FinishMessageFunc, a_TableName : str, a_KeyName, a_FieldName, a_GetButtonNameAndKeyValueAndAccessFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT, field_type = FieldType.text):
    keyboard_cancel = GetCancelKeyboardButtonsTemplate(a_AccessFunc, access_mode)
    a_Prefix = f'edit_{a_TableName}_{a_KeyName}_{a_FieldName}:'
    sel_handler = bd_item_select.SelectDBItemTemplate(a_TableName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode)
    dp.register_message_handler(sel_handler, text = a_ButtonName)
    dp.register_callback_query_handler(StartEditBDItemTemplate(a_FSM, a_EditMessageFunc, a_TableName, a_KeyName, a_FieldName, a_Prefix, a_AccessFunc, keyboard_cancel, access_mode), lambda x: x.data.startswith(a_Prefix))
    if field_type == FieldType.photo:
        dp.register_message_handler(FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode, field_type = field_type), content_types = ['photo'], state = a_FSM.item_field)
        dp.register_message_handler(FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode, field_type = field_type), content_types = ['text'], state = a_FSM.item_field)
    else:
        dp.register_message_handler(FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode, field_type = field_type), state = a_FSM.item_field)
