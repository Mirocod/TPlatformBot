# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы пользователей

from bot_sys import keyboard, user_access, bot_bd
from bot_modules import mod_simple_message
from template import simple_message, sql_request, bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMRequestToBD(StatesGroup):
    sqlRequest = State()

# ---------------------------------------------------------
# БД
module_name = 'groups'

table_groups_name = 'user_groups'
table_user_in_groups_name = 'user_in_groups'

key_table_groups_name = 'group_id'
name_table_groups_field = 'groupName'
user_id_field = 'user_id'
access_field = 'access'
create_datetime_field = 'createDateTime'

# ---------------------------------------------------------
# Сообщения

start_message = '''
<b>Группы пользователей находятся в стадии разработки</b>

Пока можете воспользоваться хардкорным способом через запросы к БД
'''

request_start_message = '''
**Задайте запрос к БД**

Можете воспользоваться следующими шаблонами:
1. `SELECT * FROM users` - Все пользователи
2. `SELECT group_id, groupName FROM user_groups` - Все группы пользоватлей
3. `INSERT INTO user_groups(groupName) VALUES('GROUPNAME')` - добавление группы с именем GROUPNAME
4. `SELECT group_id FROM user_in_groups WHERE user_id = USERID`- Все ID групп в которых состоит пользователь с USERID
5. `SELECT groupName FROM user_groups WHERE group_id=(SELECT groupid FROM user_in_groups WHERE user_id = USERID)` - Все имена групп пользователя с USERID
6. `INSERT INTO user_in_groups(user_id, group_id) VALUES(USERID, GROUPID)` - добавление пользователя USERID в группу с GROUPID
'''

help_message = '''
📄 Существует две БД для работы с группами
`user_groups (group_id, groupName)` - содержит названия групп
`user_in_groups(user_id, group_id)` - содержит соответсвия ID пользователей и групп
 '''

start_menu_button_name = "‍️️▦ Группы пользователей"
sql_request_button_name = "⛃ Запрос к БД для редактирования групп"
help_button_name = "📄 Информация по группам"

init_access = '{user_access.user_access_group_new}=-'

class ModuleGroups(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(start_message, start_menu_button_name, init_access, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_SqlRequestButtonName = self.CreateButton('sql request', sql_request_button_name)
        self.m_RequestStartMessage = self.CreateMessage('equest start', request_start_message)

        self.m_HelpButtonName = self.CreateButton('help', help_button_name)
        self.m_HelpMessage = self.CreateMessage('help', help_message)

        self.m_HelpMessageHandler = simple_message.InfoMessageTemplate(
                self.m_Bot,
                self.m_HelpMessage,
                self.m_GetStartKeyboardButtonsFunc,
                None,
                self.m_GetAccessFunc
                )

    def GetInitBDCommands(self):
        return super(). GetInitBDCommands() + [
            f"""CREATE TABLE IF NOT EXISTS {table_groups_name}(
                {key_table_groups_name} INTEGER PRIMARY KEY NOT NULL,
                {name_table_groups_field} TEXT,
                {access_field} TEXT,
                {create_datetime_field} TEXT,
                UNIQUE({key_table_groups_name}),
                UNIQUE({name_table_groups_field})
            );""",
            f"""CREATE TABLE IF NOT EXISTS {table_user_in_groups_name}(
                {user_id_field} INTEGER,
                {key_table_groups_name} INTEGER,
                {access_field} TEXT,
                {create_datetime_field} TEXT,
                UNIQUE({user_id_field}, {key_table_groups_name})
            );""",
            f"INSERT OR IGNORE INTO {table_groups_name} ({name_table_groups_field}, {access_field}, {create_datetime_field}) VALUES ('{user_access.user_access_group_new}', '{user_access.user_access_group_new}=-', {bot_bd.GetBDDateTimeNow()});"
            ]

    def GetName(self):
        return module_name

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.m_SqlRequestButtonName, user_access.AccessMode.EDIT, self.GetAccess()), 
                keyboard.ButtonWithAccess(self.m_HelpButtonName , user_access.AccessMode.VIEW, self.GetAccess())
                ]
        return mod_buttons + keyboard.MakeButtons(cur_buttons, a_UserGroups)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        sql_request.RequestToBDRegisterHandlers(
                self.m_Bot,
                self.m_SqlRequestButtonName,
                self.m_RequestStartMessage,
                FSMRequestToBD,
                self.m_GetStartKeyboardButtonsFunc,
                user_access.AccessMode.EDIT,
                self.m_GetAccessFunc
                )
        self.m_Bot.RegisterMessageHandler(
                self.m_HelpMessageHandler, 
                bd_item.GetCheckForTextFunc(self.m_HelpButtonName)
                )

