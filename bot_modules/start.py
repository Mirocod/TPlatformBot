# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Стартовое меню

from bot_sys import user_access
from bot_modules import mod_simple_message, users
from template import bd_item

module_name = 'start'

button_names = {
    mod_simple_message.ButtonNames.START: "☰ Главное меню",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>Добро пожаловать!</b>

Выберите возможные действия на кнопках ниже ⌨''',
}

init_access = f'{user_access.user_access_group_all}=+'

class ModuleStart(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        super().__init__(messages, button_names, init_access, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log)

    def GetName(self):
        return module_name

    # Основной обработчик главного сообщения
    async def StartMessageHandler(self, a_Message, state = None):
        user_id = str(a_Message.from_user.id)
        user_name = str(a_Message.from_user.username)
        first_name = str(a_Message.from_user.first_name)
        last_name = str(a_Message.from_user.last_name)
        is_bot = str(a_Message.from_user.is_bot)
        language_code = str(a_Message.from_user.language_code)
        users.AddUser(self.m_Bot, user_id, user_name, first_name, last_name, is_bot, language_code)
        self.m_Log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте. Полные данные {a_Message.from_user}.')
        return await super().StartMessageHandler(a_Message, state)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        self.m_Bot.RegisterMessageHandler(
                self.m_StartMessageHandler, 
                None,
                commands = ['start']
                )


