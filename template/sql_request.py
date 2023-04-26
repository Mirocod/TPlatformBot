# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Сообщения для работы с sql запросами

from bot_sys import bot_bd, log, config, user_access, keyboard
from bot_modules import access, groups

from aiogram import types
from aiogram.dispatcher import FSMContext

canсel_button_name = "🚫 Отменить"

cancel_message = '''
🚫 Запрос к БД отменён
'''

def GetCancelKeyboardButtons(a_UserGroups, a_AccessFunc, a_AccessMode):
    cur_buttons = [
        keyboard.ButtonWithAccess(canсel_button_name, a_AccessMode, a_AccessFunc())
    ]
    return keyboard.MakeKeyboard(cur_buttons, a_UserGroups)

def RequestToBDTemplate(a_StartMessage, a_AccessFunc, a_FSM, a_AccessMode):
    async def RequestToBDStart(a_Message : types.message):
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, a_AccessMode):
            return await a_Message.answer(access.access_denied_message, reply_markup = GetCancelKeyboardButtons(user_groups, a_AccessFunc, a_AccessMode))
        await a_FSM.sqlRequest.set()
        await a_Message.answer(a_StartMessage, reply_markup = GetCancelKeyboardButtons(user_groups, a_AccessFunc, a_AccessMode), parse_mode='Markdown')
    return RequestToBDStart

def RequestToBDFinishTemplate(a_GetButtonsFunc, a_AccessFunc, a_AccessMode):
    async def RequestToBDFinish(a_Message : types.message, state : FSMContext):
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, a_AccessMode):
            return await a_Message.answer(access.access_denied_message, reply_markup = a_GetButtonsFunc(user_groups))
        result = ''
        async with state.proxy() as prjData:
            if a_Message.text == canсel_button_name:
                await state.finish()
                return await a_Message.answer(cancel_message, reply_markup = a_GetButtonsFunc(user_groups))

            sql_request = a_Message.text
            log.Success(f'Сделан запрос [{sql_request}] пользователем {a_Message.from_user.id}.')
            result, error = bot_bd.SQLRequestToBD(sql_request, commit = True, return_error = True)
            if not error is None:
                log.Error(f'Ошибка при выполнении запроса [{sql_request}] от пользователя {a_Message.from_user.id} ответ следующий [{str(error)}].')
                result = str(error)
            else:
                log.Success(f'Результат запроса [{sql_request}] от пользователя {a_Message.from_user.id} следующий [{result}].')
        await state.finish()
        await a_Message.answer(str(result), reply_markup = a_GetButtonsFunc(user_groups))
    return RequestToBDFinish

def RequestToBDRegisterHandlers(dp, a_RequestButtonName, a_RequestStartMessage, a_FSM, a_GetButtonsFunc, a_AccessMode, a_AccessFunc):
    dp.register_message_handler(RequestToBDTemplate(a_RequestStartMessage, a_AccessFunc, a_FSM, a_AccessMode), text = a_RequestButtonName)
    dp.register_message_handler(RequestToBDFinishTemplate(a_GetButtonsFunc, a_AccessFunc, a_AccessMode), state = a_FSM.sqlRequest)
