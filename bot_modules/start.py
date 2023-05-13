# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Стартовое меню

from bot_sys import user_access
from bot_modules import mod_simple_message
from template import bd_item

start_message = '''
<b>Добро пожаловать!</b>

Выберите возможные действия на кнопках ниже ⌨'''

class ModuleStart(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        start_menu_button_name = "☰ Главное меню"
        a_InitAccess = f'{user_access.user_access_group_all}=+'
        super().__init__(start_message, start_menu_button_name, a_InitAccess, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return 'start'

    # Основной обработчик главного сообщения
    async def StartMessageHandler(self, a_Message, state = None):
        user_id = str(a_Message.from_user.id)
        user_name = str(a_Message.from_user.username)
        first_name = str(a_Message.from_user.first_name)
        last_name = str(a_Message.from_user.last_name)
        is_bot = str(a_Message.from_user.is_bot)
        language_code = str(a_Message.from_user.language_code)
        #profile.AddUser(user_id, user_name, first_name, last_name, is_bot, language_code)
        self.m_Log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте. Полные данные {a_Message.from_user}.')
        return await super().StartMessageHandler(a_Message, state)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        self.m_Bot.RegisterMessageHandler(
                self.m_StartMessageHandler, 
                None,
                commands = ['start']
                )



#def GetStartKeyboardButtons(a_Message, a_UserGroups):
#    mods = [profile, projects, groups, access, backup, languages]
#    return keyboard.MakeKeyboardForMods(mods, a_UserGroups)

