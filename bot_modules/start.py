# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Стартовое меню

from bot_sys import log, config, keyboard
from bot_modules import profile, projects, groups, access

from aiogram.dispatcher import Dispatcher

# ---------------------------------------------------------
# БД
init_bd_cmds = [
"INSERT OR IGNORE INTO module_access (modName, modAccess) VALUES ('start', 'other=+');"
]

# ---------------------------------------------------------
# Сообщения

start_message = '''
<b>👋 | Добро пожаловать!</b>

<b>Приятного пользования!</b>
'''

start_menu_button_name = "☰ Главное меню"

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons(a_UserAccess):
    mods = [profile, projects, groups, access]
    return keyboard.MakeKeyboardForMods(mods, a_UserAccess)

# ---------------------------------------------------------
# Обработка сообщений

# Первичное привестивие
async def StartMenu(a_Message):
    user_id = int(a_Message.from_user.id)
    user_access = access.GetUserAccess(user_id)
    user_name = str(a_Message.from_user.username)
    profile.AddUser(user_id, user_name)
    log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте')
    await a_Message.answer(start_message, reply_markup=GetStartKeyboardButtons(user_access), parse_mode='HTML')

# ---------------------------------------------------------
# API

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

# Имена доступных кнопок
def GetButtonNames(a_UserAccess):
    return [start_menu_button_name]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(StartMenu, commands = ['start'])
    dp.register_message_handler(StartMenu, text = start_menu_button_name)


