# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Редактирование элемента в БД

from enum import Enum

from bot_sys import user_access, bot_bd, keyboard
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

class FieldType(Enum):
    text = 0
    photo = 1

def StartEditBDItemTemplate(a_FSM, a_MessageFunc, a_TableName, a_KeyName, a_FieldName, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT):
    async def StartEditBDItem(a_CallbackQuery : types.CallbackQuery, state : FSMContext):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        await a_FSM.item_id.set()
        item_id = str(a_CallbackQuery.data).replace(a_Prefix, '')
        res_of_work_func = None
        async with state.proxy() as item_data:
            item_data['item_id'] = item_id

            check_func = bd_item.CheckAccessBDItemTemplate(a_TableName, a_KeyName, item_id, a_MessageFunc, access_mode)
            print('check_func', check_func)
            print('res_of_work_func', res_of_work_func)
            check = await check_func(a_CallbackQuery, res_of_work_func)
            print('res_of_work_func', res_of_work_func)
            print('check', check)
            if not check is None:
                return check
        await a_FSM.next()
        print('res_of_work_func', res_of_work_func)
        return res_of_work_func

    return simple_message.SimpleMessageTemplate(StartEditBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def FinishEditBDItemTemplate(a_FSM, a_TableName, a_KeyName, a_FieldName, a_MessageFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT, field_type = FieldType.text):
    async def FinishEditBDItem(a_CallbackQuery : types.CallbackQuery, state : FSMContext):
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        error = None
        res_of_work_func = None
        async with state.proxy() as item_data:
            if a_Message.text == canсel_button_name:
                return simple_message.WorkFuncResult(cancel_message)

            item_id = item_data['item_id']
            check = await bd_item.CheckAccessBDItemTemplate(a_TableName, a_KeyName, item_id, a_MessageFunc, access_mode)(a_CallbackQuery, res_of_work_func)

            if not check is None:
                return check

            field_value = ''
            if field_type == FieldType.photo:
                if a_Message.photo == None or len(a_Message.photo) == 0:
                    return simple_message.WorkFuncResult(error_photo_type_message)
                field_value = a_Message.photo[0].file_id
            else:
                field_value = a_Message.text
            res, error = bot_item.EditBDItemInTableTemplate(a_TableName, a_KeyName, a_FieldName)(item_id, field_value)
            log.Success(f'Изменено поле в таблице {a_TableName} ключу {a_KeyName}={item_id}. Новое значение поля {a_FieldName}={field_value}. Пользователь {user_id}.')
        await state.finish()
        if error:
            return simple_message.WorkFuncResult(error)
        return res_of_work_func

    return simple_message.SimpleMessageTemplate(FinishEditBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def EditBDItemRegisterHandlers(dp, a_ButtonName, a_StartMessage, a_EditMessageFunc, a_FinishMessageFunc, a_TableName : str, a_KeyName, a_FieldName, a_GetButtonNameAndKeyValueAndAccessFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.EDIT, field_type = FieldType.text):
    class FSMEditItem(StatesGroup):
        item_id = State()
        item_field = State()
    a_Prefix = f'edit_{a_TableName}_{a_KeyName}_{a_FieldName}:'
    sel_handler = bd_item_select.SelectDBItemTemplate(a_TableName, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_Prefix, access_mode)
    dp.register_message_handler(sel_handler, text = a_ButtonName)
    dp.register_callback_query_handler(StartEditBDItemTemplate(FSMEditItem, a_EditMessageFunc, a_TableName, a_KeyName, a_FieldName, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode), lambda x: x.data.startswith(a_Prefix))
    dp.register_message_handler(FinishEditBDItemTemplate(FSMEditItem, a_TableName, a_KeyName, a_FieldName, a_FinishMessageFunc, a_Prefix, a_AccessFunc, a_ButtonFunc, access_mode, field_type = field_type), state = FSMEditItem.item_field)
