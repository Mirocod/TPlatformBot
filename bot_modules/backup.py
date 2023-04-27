# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Бэкапы пользователя

from bot_sys import bot_bd, log, config, keyboard, user_access
from bot_modules import start, access, groups
from template import file_message, simple_message

from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
module_name = 'backup'

init_bd_cmds = [
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_new}=-', '{user_access.user_access_group_new}=-');"
]

# ---------------------------------------------------------
# Сообщения

backup_message = '''
<b>Здесь вы можете выполнить специальные операции по сервисному обслуживанию</b>
'''

backup_bd_message = '''
<b>📀 Резервная копия базы данных</b>
🕰 <code>@time</code>
'''

backup_log_message = '''
<b>📃 Резервная копия логов</b>
🕰 <code>@time</code>
'''

error_backup_message = '''
<b>❌ Ошибка резервного копирования</b>
'''

backup_button_name = "📦 Резервные копии и логи"
backup_bd_button_name = "📀 Резервные копия базы"
backup_log_button_name = "📃 Логи"

# ---------------------------------------------------------
# Работа с кнопками

def GetBackupKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(backup_bd_button_name, user_access.AccessMode.EDIT, GetAccess()), 
        keyboard.ButtonWithAccess(backup_log_button_name, user_access.AccessMode.EDIT, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# ---------------------------------------------------------
# Работа с базой данных пользователей

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
    dp.register_message_handler(simple_message.InfoMessageTemplate(backup_message, GetBackupKeyboardButtons, GetAccess), text = backup_button_name)

    dp.register_message_handler(file_message.BackupFileTemplate(bot_bd.GetBDFileName(), backup_bd_message, GetAccess, GetBackupKeyboardButtons, error_backup_message), text = backup_bd_button_name)
    dp.register_message_handler(file_message.BackupFileTemplate(log.g_log_file_name, backup_log_message, GetAccess, GetBackupKeyboardButtons, error_backup_message), text = backup_log_button_name)
