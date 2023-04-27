# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Простые информационные сообщения

from bot_sys import user_access, config
from bot_modules import access, groups
from aiogram import types

from aiogram import Bot
bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode = types.ParseMode.HTML)

class WorkFuncResult():
    def __init__(self, a_StringMessage : str, photo_id = None, item_access = None, keyborad_func = None):
        self.string_message = a_StringMessage
        self.photo_id = photo_id
        self.item_access = item_access
        self.keyborad_func = keyborad_func


def InfoMessageTemplate(a_HelpMessage, a_GetButtonsFunc, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    async def GetMessage(a_Message : types.message, state = None):
        return WorkFuncResult(a_HelpMessage)

    return SimpleMessageTemplate(GetMessage, a_GetButtonsFunc, a_AccessFunc, access_mode)

def SimpleMessageTemplate(a_WorkFunc, a_GetButtonsFunc, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    async def SimpleMessage(a_Message : types.message, state = None):
        user_id = str(a_Message.from_user.id)
        user_groups = groups.GetUserGroupData(user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, access_mode):
            return await bot.send_message(a_Message.from_user.id, access.access_denied_message, reply_markup = a_GetButtonsFunc(user_groups))

        res = await a_WorkFunc(a_Message, state = state)
        if res is None:
            return
        
        keyborad_func = a_GetButtonsFunc
        if res.keyborad_func:
            keyborad_func = res.keyborad_func
        
        msg = res.string_message
        if msg is None:
            return

        photo_id = res.photo_id

        if not res.item_access is None and not user_access.CheckAccessString(res.item_access, user_groups, access_mode):
            return await bot.send_message(a_Message.from_user.id, access.access_denied_message, reply_markup = keyborad_func(user_groups))

        if photo_id is None or photo_id == 0 or photo_id == '0':
            return await bot.send_message(a_Message.from_user.id, msg, reply_markup = keyborad_func(user_groups))

        await bot.send_photo(user_id, photo_id, msg, reply_markup = keyborad_func(user_groups))
    return SimpleMessage
