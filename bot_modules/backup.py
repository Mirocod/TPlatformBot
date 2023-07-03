# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Бэкапы пользователя

from bot_sys import user_access, keyboard
from bot_modules import mod_simple_message, profile
from template import bd_item, file_message

# ---------------------------------------------------------
# БД
module_name = 'backup'

# ---------------------------------------------------------
# Сообщения
start_message = '''
<b>Здесь вы можете выполнить специальные операции по сервисному обслуживанию</b>
'''

start_button_name = "📦 Резервные копии и логи"

backup_bd_message = '''
<b>📀 Резервная копия базы данных</b>
🕰 <code>@time</code>
'''

backup_log_message = '''
<b>📃 Резервная копия логов</b>
🕰 <code>@time</code>
'''

error_backup_message = '''
<b>❌ Ошибка резервного копирования</b>
'''

backup_bd_button_name = "📀 Резервные копия базы"
backup_log_button_name = "📃 Логи"

button_names = {
    mod_simple_message.ButtonNames.START: start_button_name,
}

messages = {
    mod_simple_message.Messages.START: start_message,
}

init_access = f'{user_access.user_access_group_new}=-'

class ModuleBackup(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        super().__init__(messages, button_names, init_access, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log)
        self.m_BackupBDButtonName = self.CreateButton('backup bd', backup_bd_button_name)
        self.m_BackupBDMessage = self.CreateMessage('backup bd', backup_bd_message)

        self.m_BackupLogButtonName = self.CreateButton('backup log', backup_log_button_name)
        self.m_BackupLogMessage = self.CreateMessage('backup log', backup_log_message)

        self.m_BackupErrorMessage = self.CreateMessage('backup error', error_backup_message)

        self.m_BackupBDMessageHandler = file_message.BackupFileTemplate(
                self.m_Bot,
                self.m_Bot.m_BDFileName,
                self.m_BackupBDMessage,
                self.m_GetAccessFunc,
                self.m_GetStartKeyboardButtonsFunc,
                None,
                self.m_BackupErrorMessage,
                access_mode = user_access.AccessMode.EDIT
                )
        self.m_BackupLogMessageHandler = file_message.BackupFileTemplate(
                self.m_Bot,
                self.m_Bot.GetLog().GetFileName(),
                self.m_BackupLogMessage,
                self.m_GetAccessFunc,
                self.m_GetStartKeyboardButtonsFunc,
                None,
                self.m_BackupErrorMessage,
                access_mode = user_access.AccessMode.EDIT
                )

    def GetName(self):
        return module_name

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.m_BackupBDButtonName, user_access.AccessMode.EDIT, self.GetAccess()), 
                keyboard.ButtonWithAccess(self.m_BackupLogButtonName , user_access.AccessMode.EDIT, self.GetAccess())
                ]
        return mod_buttons + keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        self.m_Bot.RegisterMessageHandler(
                self.m_BackupBDMessageHandler, 
                bd_item.GetCheckForTextFunc(self.m_BackupBDButtonName)
                )
        self.m_Bot.RegisterMessageHandler(
                self.m_BackupLogMessageHandler, 
                bd_item.GetCheckForTextFunc(self.m_BackupLogButtonName)
                )
