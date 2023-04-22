# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Стартовое меню

from bot_sys import log, config, keyboard
from bot_modules import profile

from aiogram.dispatcher import Dispatcher

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
    profile_button_names = profile.GetButtonNames(a_UserAccess)
    return keyboard.MakeKeyboard([profile_button_names])

# ---------------------------------------------------------
# Обработка сообщений

# Первичное привестивие
async def StartMenu(a_Message):
    user_id = int(a_Message.from_user.id)
    user_name = str(a_Message.from_user.username)
    profile.AddUser(user_id, user_name)
    log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте')
    await a_Message.answer(start_message, reply_markup=GetStartKeyboardButtons(None), parse_mode='HTML')

# ---------------------------------------------------------
# API

# Доступные кнопки
def GetInitBDCommands():
    return None

# Имена доступных кнопок
def GetButtonNames(a_UserAccess):
    return start_menu_button_name

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(StartMenu, commands = ['start'])
    dp.register_message_handler(StartMenu, text = start_menu_button_name)


