# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Бэкапы пользователя

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, access, groups
from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
module_name = 'backup'

init_bd_cmds = [
f"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('{module_name}', 'other=+');"
]

# ---------------------------------------------------------
# Сообщения

backup_message = '''
<b>Здесь вы можете выполнить специальные операции по сервисному обслуживанию</b>
'''

backup_bd_message = '''
<b>📦 Резервная копия базы данных</b>
🕰 <code>@time</code>
'''

backup_log_message = '''
<b>📦 Резервная копия логов</b>
🕰 <code>@time</code>
'''

error_backup_message = '''
<b>📦 Ошибка резервного копирования</b>
'''

backup_button_name = "📰 Резервные копии и логи"
backup_bd_button_name = "📰 Резервные копия базы"
backup_log_button_name = "📰 Логи"

# ---------------------------------------------------------
# Работа с кнопками

def GetBackupKeyboardButtons(a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(backup_bd_button_name, user_access.AccessMode.EDIT, GetAccess()), 
        keyboard.ButtonWithAccess(backup_log_button_name, user_access.AccessMode.EDIT, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

async def BackupOpen(a_Message):
    user_id = str(a_Message.from_user.id)
    user_groups= groups.GetUserGroupData(user_id)
    if not user_access.CheckAccessString(GetAccess(), user_groups, user_access.AccessMode.VIEW):
        return await bot.send_message(user_id, access.access_denied_message, reply_markup = GetBackupKeyboardButtons(user_groups))

    await bot.send_message(user_id, backup_message, reply_markup = GetBackupKeyboardButtons(user_groups))

def BackupFileTemplate(a_Path, a_CaptionMessage, a_AccessFunc, a_ButtonFunc, a_ErrorMessage):
    async def BackupFile(a_Message):
        user_id = str(a_Message.from_user.id)
        user_groups= groups.GetUserGroupData(user_id)
        if not user_access.CheckAccessString(a_AccessFunc(), user_groups, user_access.AccessMode.EDIT):
            return await bot.send_message(user_id, access.access_denied_message, reply_markup = a_ButtonFunc(user_groups))

        document = await GetFile(a_Path)
        if document is None:
            return await bot.send_message(user_id, error_backup_message, reply_markup = a_ButtonFunc(user_groups))

        await bot.send_document(user_id, document, caption = a_CaptionMessage.replace('@time', log.GetTime()), reply_markup = a_ButtonFunc(user_groups))
    return BackupFile

# ---------------------------------------------------------
# Работа с базой данных пользователей

async def GetFile(a_Path):
    try:
        document = open(a_Path, 'rb')
        log.Success(f'Загружен файл {a_Path}')
        return document
    except Exception as e:
        log.Error(f'Не удалось загрузить файл {a_Path}. Ошибка {str(e)}')
        return None

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(backup_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(BackupOpen, text = backup_button_name)
    dp.register_message_handler(BackupFileTemplate(bot_bd.GetBDFileName(), backup_bd_message, GetAccess, GetBackupKeyboardButtons, error_backup_message), text = backup_bd_button_name)
    dp.register_message_handler(BackupFileTemplate(log.g_log_file_name, backup_log_message, GetAccess, GetBackupKeyboardButtons, error_backup_message), text = backup_log_button_name)
