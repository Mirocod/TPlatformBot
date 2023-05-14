# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Сообщения для работы с файлами

from bot_sys import log, config, user_access
from bot_modules import access, groups
from template import simple_message

def BackupFileTemplate(a_Bot, a_Path, a_CaptionMessage, a_AccessFunc, a_GetButtonsFunc, a_GetInlineButtonsFunc, a_ErrorMessage, access_mode = user_access.AccessMode.EDIT):
    async def BackupFile(a_Message):
        user_id = str(a_Message.from_user.id)
        user_groups= groups.GetUserGroupData(a_Bot, user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, access_mode):
            return await simple_message.AccessDeniedMessage(a_Bot, a_GetButtonsFunc, user_id, a_Message, user_groups)

        document = await GetFile(a_Bot, a_Path)
        if document is None:
            return a_Bot.SendMessage(
                user_id,
                a_ErrorMessage,
                None,
                simple_message.ProxyGetButtonsTemplate(a_GetButtonsFunc)(a_Message, user_groups),
                None
                )
        msg = a_CaptionMessage.GetDesc()
        msg = msg.replace('@time', a_Bot.GetLog().GetTime())

        await a_Bot.SendDocument(
                user_id,
                document,
                msg,
                simple_message.ProxyGetButtonsTemplate(a_GetButtonsFunc)(a_Message, user_groups),
                simple_message.ProxyGetButtonsTemplate(a_GetInlineButtonsFunc)(a_Message, user_groups)
                )
    return BackupFile

async def GetFile(a_Bot, a_Path):
    try:
        document = open(a_Path, 'rb')
        a_Bot.GetLog().Success(f'Загружен файл {a_Path}')
        return document
    except Exception as e:
        a_Bot.GetLog().Error(f'Не удалось загрузить файл {a_Path}. Ошибка {str(e)}')
        return None
