# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import bot_bd, log, config, keyboard, user_access, user_messages
from bot_modules import start, access, groups
from template import simple_message

from aiogram import types
from aiogram.dispatcher import Dispatcher

# ---------------------------------------------------------
# БД
module_name = 'profile'

table_name = 'users'
key_name = 'user_id'
name_field = 'userName'
name1_field = 'userFirstName'
name2_field = 'userLastName'
is_bot_field = 'userIsBot'
language_code_field = 'userLanguageCode'
access_field = 'userAccess'
create_datetime_field = 'createDateTime'

init_bd_cmds = [f"""CREATE TABLE IF NOT EXISTS {table_name}(
    {key_name} INTEGER,
    {name_field} TEXT,
    {name1_field} TEXT,
    {name2_field} TEXT,
    {is_bot_field} TEXT,
    {language_code_field} TEXT,
    {access_field} TEXT,
    {create_datetime_field} TEXT,
    UNIQUE({key_name})
);""",
f"INSERT OR IGNORE INTO module_access (modName, modAccess, itemDefaultAccess) VALUES ('{module_name}', '{user_access.user_access_group_new}=+', '{user_access.user_access_group_new}=+');"
]

def MSG(a_MessageName, a_MessageDesc):
    def UpdateMSG(a_Message : user_messages.Message):
        print(a_Message.m_MessageName, a_Message.m_MessageDesc)
        globals()[a_Message.m_MessageName] = a_Message
    user_messages.MSG(a_MessageName, a_MessageDesc, UpdateMSG, log.GetTimeNow())

# ---------------------------------------------------------
# Сообщения

MSG('profile_message', f'''
<b>📰 Профиль:</b> 

<b>ID:</b> #{key_name}
<b>Имя:</b> #{name_field}
<b>Имя1:</b> #{name1_field}
<b>Имя2:</b> #{name2_field}
<b>Код языка:</b> #{language_code_field}
<b>Дата добавления:</b> #{create_datetime_field}
''')

user_profile_button_name = "📰 Профиль"

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons(a_Message, a_UserGroups):
    mods = [start]
    return keyboard.MakeKeyboardForMods(mods, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

async def ProfileOpen(a_Message, state = None):
    user_info = GetUserInfo(a_Message.from_user.id)
    msg = profile_message
    if not user_info is None:
        msg = str(msg).\
                replace(f'#{key_name}', str(user_info[0])).\
                replace(f'#{name_field}', str(user_info[1])).\
                replace(f'#{name1_field}', str(user_info[2])).\
                replace(f'#{name2_field}', str(user_info[3])).\
                replace(f'#{is_bot_field}', str(user_info[4])).\
                replace(f'#{language_code_field}', str(user_info[5])).\
                replace(f'#{access_field}', str(user_info[6])).\
                replace(f'#{create_datetime_field}', str(user_info[7]))
        return simple_message.WorkFuncResult(msg, item_access = str(user_info[6]))
    return simple_message.WorkFuncResult(msg)

# ---------------------------------------------------------
# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_UserID, a_UserName, a_UserName1, a_UserName2, a_UserIsBot, a_LanguageCode):
    bot_bd.SQLRequestToBD(f"INSERT OR IGNORE INTO users ({key_name}, {name_field}, {name1_field}, {name2_field}, {is_bot_field}, {language_code_field}, {access_field}, {create_datetime_field}) VALUES (?, ?, ?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()});", 
            commit=True, param = (a_UserID, a_UserName, a_UserName1, a_UserName2, a_UserIsBot, a_LanguageCode, access.GetItemDefaultAccessForModule(module_name)))

    user_groups = groups.GetUserGroupData(a_UserID)
    # Если пользователь не состоит ни в одной группе, то добавляем его в группу user_access.user_access_group_new
    if len(user_groups.group_names_list) == 0:
        new_group_id = bot_bd.SQLRequestToBD(f'SELECT {groups.key_table_groups_name} FROM {groups.table_groups_name} WHERE {groups.name_table_groups_field} = ?', 
                param = [user_access.user_access_group_new])
        if new_group_id and new_group_id[0]:
            bot_bd.SQLRequestToBD(f"INSERT OR IGNORE INTO {groups.table_user_in_groups_name} ({groups.user_id_field}, {groups.key_table_groups_name}, {groups.access_field}, {groups.create_datetime_field}) VALUES (?, ?, ?, {bot_bd.GetBDDateTimeNow()});", 
                    commit=True, param = (a_UserID, new_group_id[0][0], access.GetItemDefaultAccessForModule(module_name)))

def GetUserInfo(a_UserID):
    user_info = bot_bd.SQLRequestToBD('SELECT * FROM users WHERE user_id = ?', param = [a_UserID])
    if len(user_info) != 0:
        return user_info[0]
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
    return [keyboard.ButtonWithAccess(user_profile_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(simple_message.SimpleMessageTemplate(ProfileOpen, GetStartKeyboardButtons, GetAccess), text = user_profile_button_name)
