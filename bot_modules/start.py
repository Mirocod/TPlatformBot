# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Стартовое меню

from bot_sys import log, config, keyboard, user_access, user_messages
from bot_modules import profile, projects, groups, access, backup, languages
from template import simple_message

from aiogram.dispatcher import Dispatcher

def MSG(a_MessageName, a_MessageDesc):
    def UpdateMSG(a_Message : user_messages.Message):
        print(a_Message.m_MessageName, a_Message.m_MessageDesc)
        globals()[a_Message.m_MessageName] = a_Message
    user_messages.MSG(a_MessageName, a_MessageDesc, UpdateMSG, log.GetTimeNow())

# ---------------------------------------------------------
# БД
module_name = 'start'

init_bd_cmds = [
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_all}=+', '{user_access.user_access_group_all}=+');"
]

# ---------------------------------------------------------
# Сообщения

MSG('start_message', '''
<b>Добро пожаловать!</b>

Выберите возможные действия на кнопках ниже ⌨'''
)

start_menu_button_name = "☰ Главное меню"

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons(a_Message, a_UserGroups):
    mods = [profile, projects, groups, access, backup, languages]
    return keyboard.MakeKeyboardForMods(mods, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

# Первичное привестивие
async def StartMenu(a_Message, state = None):
    user_id = str(a_Message.from_user.id)
    user_name = str(a_Message.from_user.username)
    first_name = str(a_Message.from_user.first_name)
    last_name = str(a_Message.from_user.last_name)
    is_bot = str(a_Message.from_user.is_bot)
    language_code = str(a_Message.from_user.language_code)
    profile.AddUser(user_id, user_name, first_name, last_name, is_bot, language_code)
    log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте. Полные данные {a_Message.from_user}.')
    return simple_message.WorkFuncResult(start_message)

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
    dp.register_message_handler(simple_message.SimpleMessageTemplate(StartMenu, GetStartKeyboardButtons, GetAccess), commands = ['start'])
    dp.register_message_handler(simple_message.SimpleMessageTemplate(StartMenu, GetStartKeyboardButtons, GetAccess), text = start_menu_button_name)


