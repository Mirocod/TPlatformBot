# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы пользователей

from bot_sys import keyboard, user_access, bot_bd
from bot_modules import mod_simple_message, users, groups, user_in_groups
from template import simple_message, sql_request, bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMRequestToBD(StatesGroup):
    sqlRequest = State()

# ---------------------------------------------------------
# БД
module_name = 'users_groups_agregator'

# ---------------------------------------------------------
# Сообщения

request_start_message = f'''
**Задайте запрос к БД**

Можете воспользоваться следующими шаблонами:
1. `SELECT * FROM {users.table_name}` - Все пользователи
2. `SELECT {groups.key_name}, {groups.name_field} FROM {groups.table_name}` - Все группы пользоватлей
3. `INSERT INTO {groups.table_name}({groups.name_field}) VALUES('GROUPNAME')` - добавление группы с именем GROUPNAME
4. `SELECT {user_in_groups.parent_id_field} FROM {user_in_groups.table_name} WHERE {user_in_groups.name_field} = USERID`- Все ID групп в которых состоит пользователь с USERID
5. `SELECT {groups.name_field} FROM {groups.table_name} WHERE {groups.name_field}=(SELECT groupid FROM {user_in_groups.table_name} WHERE {user_in_groups.name_field} = USERID)` - Все имена групп пользователя с USERID
6. `INSERT INTO {user_in_groups.table_name}({user_in_groups.name_field}, {user_in_groups.parent_id_field}) VALUES(USERID, GROUPID)` - добавление пользователя USERID в группу с GROUPID
'''

help_message = '''
📄 Существует две БД для работы с группами
`user_groups (group_id, groupName)` - содержит названия групп
`user_in_groups(user_id, group_id)` - содержит соответсвия ID пользователей и групп
 '''

sql_request_button_name = "⛃ Запрос к БД для редактирования групп"
help_button_name = "📄 Информация по группам"

button_names = {
    mod_simple_message.ButtonNames.START: "‍️️▦ Группы и пользователи",
}

messages = {
    mod_simple_message.Messages.START: '''
<b>Группы пользователей находятся в стадии разработки</b>

Пока можете воспользоваться хардкорным способом через запросы к БД
''',
}

init_access = f'{user_access.user_access_group_new}=-'

class ModuleUsersGroupsAgregator(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        super().__init__(messages, button_names, init_access, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log)
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

    def GetName(self):
        return module_name

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.m_SqlRequestButtonName, user_access.AccessMode.EDIT, self.GetAccess()), 
                keyboard.ButtonWithAccess(self.m_HelpButtonName , user_access.AccessMode.VIEW, self.GetAccess())
                ]
        return mod_buttons + keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)

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

