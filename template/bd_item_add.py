# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Добавление элемента в БД

from bot_sys import user_access, bot_bd, log
from bot_modules import access, groups
from template import simple_message, bd_item_select, bd_item

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


cancel_message = '''
🚫 Добавление отменено
'''

parent_id_field_name = 'parent_id'

def StartAddBDItemTemplate(a_FSM, a_FSMStart, a_MessageFunc, a_ParentTableName, a_ParentKeyFieldName, a_Prefix, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = user_access.AccessMode.EDIT):
    async def StartAddBDItem(a_CallbackQuery : types.CallbackQuery, state : FSMContext):
        user_id = str(a_CallbackQuery.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        parent_id = bd_item.GetKeyDataFromCallbackMessage(a_CallbackQuery, a_Prefix)
        res_of_work_func = None
        check = None

        await a_FSMStart.set()
        async with state.proxy() as item_data:
            item_data[parent_id_field_name] = parent_id

            if parent_id:
                check, res_of_work_func = await bd_item.CheckAccessBDItemTemplate(a_ParentTableName, a_ParentKeyFieldName, parent_id, a_MessageFunc, access_mode)(a_CallbackQuery)
            else:
                res_of_work_func = await a_MessageFunc(a_CallbackQuery)
            
            if not check is None:
                await state.finish()
                check.keyboard_func = a_FinishButtonFunc
                return check
        if parent_id:
            await a_FSM.next()
        return res_of_work_func
    return simple_message.SimpleMessageTemplate(StartAddBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def FinishAddBDItemTemplate(a_FSM, a_AddBDItemFunc, a_ParentTableName, a_ParentKeyFieldName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = user_access.AccessMode.ADD, field_type = bd_item.FieldType.text):
    return FinishOrNextAddBDItemTemplate(a_FSM, a_AddBDItemFunc, a_ParentTableName, a_ParentKeyFieldName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, True, access_mode = access_mode, field_type = field_type)

def NextAddBDItemTemplate(a_FSM, a_AddBDItemFunc, a_ParentTableName, a_ParentKeyFieldName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, access_mode = user_access.AccessMode.ADD, field_type = bd_item.FieldType.text):
    return FinishOrNextAddBDItemTemplate(a_FSM, a_AddBDItemFunc, a_ParentTableName, a_ParentKeyFieldName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, False, access_mode = access_mode, field_type = field_type)

def FinishOrNextAddBDItemTemplate(a_FSM, a_AddBDItemFunc, a_ParentTableName, a_ParentKeyFieldName, a_FieldName, a_MessageFunc, a_AccessFunc, a_ButtonFunc, a_FinishButtonFunc, a_Finish, access_mode = user_access.AccessMode.ADD, field_type = bd_item.FieldType.text):
    async def FinishAddBDItem(a_Message : types.CallbackQuery, state : FSMContext):
        state_func = None
        if a_Finish:
            state_func = state.finish
        else:
            state_func = a_FSM.next
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        error = None
        res_of_work_func = None
        check = None
        async with state.proxy() as item_data:
            if a_Message.text == bd_item.canсel_button_name:
                await state.finish()
                return simple_message.WorkFuncResult(cancel_message, keyborad_func = a_FinishButtonFunc)

            parent_id = item_data[parent_id_field_name]
            if parent_id:
                check, res_of_work_func = await bd_item.CheckAccessBDItemTemplate(a_ParentTableName, a_ParentKeyFieldName, parent_id, a_MessageFunc, access_mode)(a_Message)
            else:
                res_of_work_func = await a_MessageFunc(a_Message)

            if not check is None:
                await state_func()
                return check

            field_value = ''
            if field_type == bd_item.FieldType.photo:
                if a_Message.text == bd_item.skip_button_name:
                    field_value = '0'
                else:
                    if a_Message.photo == None or len(a_Message.photo) == 0:
                        await state.finish()
                        return simple_message.WorkFuncResult(error_photo_type_message, keyborad_func = a_FinishButtonFunc)
                    field_value = a_Message.photo[0].file_id
            else:
                field_value = a_Message.text
            item_data[a_FieldName] = field_value
            if a_Finish:
                res, error = a_AddBDItemFunc(item_data)
        await state_func()
        if error:
            return simple_message.WorkFuncResult(error)
        return res_of_work_func

    return simple_message.SimpleMessageTemplate(FinishAddBDItem, a_ButtonFunc, a_AccessFunc, access_mode)

def AddBDItem3RegisterHandlers(dp, a_StartCheckFunc, a_FSM, a_FSMName, a_FSMDesc, a_FSMPhoto, a_AddBDItemFunc, a_AddNameMessageFunc, a_AddDescMessageFunc, a_AddPhotoMessageFunc, a_FinishMessageFunc, a_ParentTableName : str, a_ParentKeyFieldName, a_NameField, a_DescField, a_PhotoField, a_GetButtonNameAndKeyValueAndAccessFunc, a_AccessFunc, a_ButtonFunc, access_mode = user_access.AccessMode.ADD):
    keyboard_cancel = bd_item.GetCancelKeyboardButtonsTemplate(a_AccessFunc, access_mode)
    keyboard_skip_and_cancel = bd_item.GetSkipAndCancelKeyboardButtonsTemplate(a_AccessFunc, access_mode)
    a_Prefix = f'add_{a_ParentTableName}_{a_ParentKeyFieldName}_{a_NameField}_{a_DescField}_{a_PhotoField}:'
    dp.register_message_handler(StartAddBDItemTemplate(a_FSM, a_FSMName, a_AddNameMessageFunc, a_ParentTableName, a_ParentKeyFieldName, a_Prefix, a_AccessFunc, keyboard_cancel, a_ButtonFunc, access_mode), a_StartCheckFunc)
    dp.register_message_handler(NextAddBDItemTemplate(a_FSM, None, a_ParentTableName, a_ParentKeyFieldName, a_NameField, a_AddDescMessageFunc, a_AccessFunc, keyboard_cancel, a_ButtonFunc, access_mode, field_type = bd_item.FieldType.text), state = a_FSMName)
    dp.register_message_handler(NextAddBDItemTemplate(a_FSM, None, a_ParentTableName, a_ParentKeyFieldName, a_DescField, a_AddPhotoMessageFunc, a_AccessFunc, keyboard_skip_and_cancel, a_ButtonFunc, access_mode, field_type = bd_item.FieldType.text), state = a_FSMDesc)
    dp.register_message_handler(FinishAddBDItemTemplate(a_FSM, a_AddBDItemFunc, a_ParentTableName, a_ParentKeyFieldName, a_PhotoField, a_FinishMessageFunc, a_AccessFunc, a_ButtonFunc, a_ButtonFunc, access_mode, field_type = bd_item.FieldType.photo), content_types = ['photo', 'text'], state = a_FSMPhoto)
