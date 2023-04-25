# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Стартовое меню

from bot_sys import log, config, keyboard, user_access
from bot_modules import profile, projects, groups, access, backup

from aiogram.dispatcher import Dispatcher

# ---------------------------------------------------------
# БД
module_name = 'start'

init_bd_cmds = [
f"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('{module_name}', 'other=+');"
]

# ---------------------------------------------------------
# Сообщения

start_message = '''
<b>👋 | Добро пожаловать!</b>

<b>Приятного пользования!</b>
'''

start_menu_button_name = "≣ Главное меню"

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons(a_UserGroups):
    mods = [profile, projects, groups, access, backup]
    return keyboard.MakeKeyboardForMods(mods, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# Первичное привестивие
async def StartMenu(a_Message):
    user_id = int(a_Message.from_user.id)
    user_groups = groups.GetUserGroupData(user_id)
    if not user_access.CheckAccessString(GetAccess(), user_groups, user_access.AccessMode.VIEW):
        return await bot.send_message(user_id, access.access_denied_message, reply_markup = GetStartKeyboardButtons(user_groups))

    user_name = str(a_Message.from_user.username)
    profile.AddUser(user_id, user_name)
    log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте')
    await a_Message.answer(start_message, reply_markup=GetStartKeyboardButtons(user_groups), parse_mode='HTML')

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Имена доступных кнопок
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(start_menu_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(StartMenu, commands = ['start'])
    dp.register_message_handler(StartMenu, text = start_menu_button_name)


