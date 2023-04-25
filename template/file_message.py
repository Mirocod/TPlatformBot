# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Сообщения для работы с файлами

from bot_sys import log, config, user_access
from bot_modules import access, groups
from aiogram import Bot, types

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

def BackupFileTemplate(a_Path, a_CaptionMessage, a_AccessFunc, a_ButtonFunc, a_ErrorMessage):
    async def BackupFile(a_Message):
        user_id = str(a_Message.from_user.id)
        user_groups= groups.GetUserGroupData(user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, user_access.AccessMode.EDIT):
            return await a_Message.answer(access.access_denied_message, reply_markup = a_ButtonFunc(user_groups))

        document = await GetFile(a_Path)
        if document is None:
            return await a_Message.answer(user_id, error_backup_message, reply_markup = a_ButtonFunc(user_groups))

        await bot.send_document(user_id, document, caption = a_CaptionMessage.replace('@time', log.GetTime()), reply_markup = a_ButtonFunc(user_groups))
    return BackupFile

async def GetFile(a_Path):
    try:
        document = open(a_Path, 'rb')
        log.Success(f'Загружен файл {a_Path}')
        return document
    except Exception as e:
        log.Error(f'Не удалось загрузить файл {a_Path}. Ошибка {str(e)}')
        return None
