# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Простые информационные сообщения

from bot_sys import user_access
from bot_modules import access, groups
from aiogram import types

def InfoMessageTemplate(a_HelpMessage, a_GetButtonsFunc, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    async def GetMessage(a_Message : types.message):
        return a_HelpMessage

    return SimpleMessageTemplate(GetMessage, a_GetButtonsFunc, a_AccessFunc, access_mode)

def SimpleMessageTemplate(a_WorkFunc, a_GetButtonsFunc, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    async def SimpleMessage(a_Message : types.message):
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, access_mode):
            return await a_Message.answer(access.access_denied_message, reply_markup = a_GetButtonsFunc(user_groups))
        
        msg = await a_WorkFunc(a_Message)
        if not msg is None:
            await a_Message.answer(msg, reply_markup = a_GetButtonsFunc(user_groups))
    return SimpleMessage
