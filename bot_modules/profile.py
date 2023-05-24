# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import user_access, bot_bd, bd_table
from bot_modules import mod_simple_message, access, access_utils, groups_utils, users
from template import bd_item, simple_message

# ---------------------------------------------------------
# БД
module_name = 'profile'

button_names = {
    mod_simple_message.ButtonNames.START: "📰 Профиль",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>📰 Профиль:</b> 

<b>ID:</b> #{users.key_name}
<b>Имя:</b> #{users.name_field}
<b>Имя1:</b> #{users.name1_field}
<b>Имя2:</b> #{users.name2_field}
<b>Код языка:</b> #{users.language_code_field}
<b>Дата добавления:</b> #{users.create_datetime_field}
''',
}

init_access = f'{user_access.user_access_group_new}=+'

class ModuleProfile(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(messages, button_names, init_access, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name

    # Основной обработчик главного сообщения
    async def StartMessageHandler(self, a_Message, state = None):
        user_info = users.GetUserInfo(self.m_Bot, a_Message.from_user.id)
        lang = str(a_Message.from_user.language_code)
        if not user_info is None:
            msg = self.GetMessage(mod_simple_message.Messages.START)
            msg = msg.GetMessageForLang(lang).StaticCopy()
            msg.UpdateDesc(users.table.ReplaceAllFieldTags(msg.GetDesc(), user_info))
            return simple_message.WorkFuncResult(msg, item_access = str(user_info[users.table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]))
        return await super().StartMessageHandler(a_Message, state)


