# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Сообщения для работы с sql запросами

from bot_sys import user_access, keyboard, bot_messages
from bot_modules import groups_utils
from template import bd_item, simple_message

canсel_button_name = "🚫 Отменить"

cancel_message = '''
🚫 Запрос к БД отменён
'''

def GetCancelKeyboardButtonsTemplate(a_AccessFunc, a_AccessMode):
    def GetCancelKeyboardButtons(a_Message, a_UserGroups):
        print ('canсel_button_name', canсel_button_name)
        cur_buttons = [
            keyboard.ButtonWithAccess(canсel_button_name, a_AccessMode, a_AccessFunc())
        ]
        return keyboard.MakeButtons(cur_buttons, a_UserGroups)
    return GetCancelKeyboardButtons

# TODO CheckAccessString -> CheckAccess

def RequestToBDTemplate(a_Bot, a_StartMessage, a_GetButtonsFunc, a_AccessFunc, a_FSM, a_AccessMode):
    async def RequestToBDStart(a_Message):
        user_id = str(a_Message.from_user.id)
        user_groups = groups_utils.GetUserGroupData(a_Bot, user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, a_AccessMode):
            return await simple_message.AccessDeniedMessage(a_Bot, a_GetButtonsFunc, user_id, a_Message, user_groups)

        await a_FSM.sqlRequest.set()
        print ('a_FSM.sqlRequest.set()', a_StartMessage)
        await simple_message.SendMessage(a_Bot, a_StartMessage, GetCancelKeyboardButtonsTemplate(a_AccessFunc, a_AccessMode), None, user_id, a_Message, user_groups, parse_mode='Markdown')
    return RequestToBDStart

def RequestToBDFinishTemplate(a_Bot, a_GetButtonsFunc, a_AccessFunc, a_AccessMode):
    async def RequestToBDFinish(a_Message, state):
        user_id = str(a_Message.from_user.id)
        user_groups = groups_utils.GetUserGroupData(a_Bot, user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, a_AccessMode):
            return await simple_message.AccessDeniedMessage(a_Bot, a_GetButtonsFunc, user_id, a_Message, user_groups)

        result = ''
        async with state.proxy() as prjData:
            if a_Message.text == canсel_button_name:
                await state.finish()
                return await simple_message.SendMessage(a_Bot, bot_messages.MakeBotMessage(cancel_message), a_GetButtonsFunc, None, user_id, a_Message, user_groups)

            sql_request = a_Message.text
            a_Bot.GetLog().Success(f'Сделан запрос [{sql_request}] пользователем {a_Message.from_user.id}.')
            result, error = a_Bot.SQLRequest(sql_request, commit = True, return_error = True)
            if not error is None:
                a_Bot.GetLog().Error(f'Ошибка при выполнении запроса [{sql_request}] от пользователя {a_Message.from_user.id} ответ следующий [{str(error)}].')
                result = str(error)
            else:
                a_Bot.GetLog().Success(f'Результат запроса [{sql_request}] от пользователя {a_Message.from_user.id} следующий [{result}].')
        await state.finish()
        await simple_message.SendMessage(a_Bot, bot_messages.MakeBotMessage(str(result)), a_GetButtonsFunc, None, user_id, a_Message, user_groups)

    return RequestToBDFinish

def RequestToBDRegisterHandlers(a_Bot, a_RequestButtonName, a_RequestStartMessage, a_FSM, a_GetButtonsFunc, a_AccessMode, a_AccessFunc):
    a_Bot.RegisterMessageHandler(RequestToBDTemplate(a_Bot, a_RequestStartMessage, a_GetButtonsFunc, a_AccessFunc, a_FSM, a_AccessMode), bd_item.GetCheckForTextFunc(a_RequestButtonName))
    a_Bot.RegisterMessageHandler(RequestToBDFinishTemplate(a_Bot, a_GetButtonsFunc, a_AccessFunc, a_AccessMode), None, state = a_FSM.sqlRequest)
