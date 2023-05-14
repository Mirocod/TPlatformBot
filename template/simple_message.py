# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Простые информационные сообщения

from bot_sys import user_access
from bot_modules import access, groups
from aiogram import types

def ProxyGetButtonsTemplate(a_GetButtonsFunc1):
    def ReturnNone(a_Message, user_groups):
        return None
    if a_GetButtonsFunc1:
        return a_GetButtonsFunc1
    else:
        return ReturnNone

async def AccessDeniedMessage(a_Bot, a_GetButtonsFunc, a_UserID, a_Message, user_groups):
    return a_Bot.SendMessage(
                a_UserID,
                access.access_denied_message,
                None,
                ProxyGetButtonsTemplate(a_GetButtonsFunc)(a_Message, user_groups),
                None
                )

class WorkFuncResult():
    def __init__(self, a_BotMessage, item_access = None):
        self.m_BotMessage = a_BotMessage
        self.item_access = item_access

def InfoMessageTemplate(a_Bot, a_HelpMessage, a_GetButtonsFunc, a_GetInlineButtonsFunc, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    async def GetMessage(a_Message : types.message, state = None):
        return WorkFuncResult(a_HelpMessage)

    return SimpleMessageTemplate(a_Bot, GetMessage, a_GetButtonsFunc, a_GetInlineButtonsFunc, a_AccessFunc, access_mode = access_mode)

def SimpleMessageTemplate(a_Bot, a_WorkFunc, a_GetButtonsFunc, a_GetInlineButtonsFunc, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    async def SimpleMessage(a_Message : types.message, state = None):
        user_id = str(a_Message.from_user.id)
        lang = str(a_Message.from_user.language_code)
        user_groups = groups.GetUserGroupData(a_Bot, user_id)
        if not user_access.CheckAccess(a_Bot.GetRootIDs(), a_AccessFunc(), user_groups, access_mode):
            return await AccessDeniedMessage(a_Bot, a_GetButtonsFunc, user_id, a_Message, user_groups)

        res = await a_WorkFunc(a_Message, state = state)
        if res is None:
            return

        msg = res.m_BotMessage
        if msg is None:
            return

        if not res.item_access is None and not user_access.CheckAccess(a_Bot.GetRootIDs(), res.item_access, user_groups, access_mode):
            return await AccessDeniedMessage(a_Bot, a_GetButtonsFunc, user_id, a_Message, user_groups)

        msg = msg.GetMessageForLang(lang).StaticCopy()

        await a_Bot.SendMessage(
                    user_id,
                    msg.GetDesc(),
                    msg.GetPhotoID(),
                    ProxyGetButtonsTemplate(a_GetButtonsFunc)(a_Message, user_groups),
                    ProxyGetButtonsTemplate(a_GetInlineButtonsFunc)(a_Message, user_groups)
                    )
    return SimpleMessage
